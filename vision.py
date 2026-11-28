import cv2
import mediapipe as mp
import time

# 모델 파일 경로를 지정하는 클래스
BaseOptions = mp.tasks.BaseOptions
# 얼굴 분석 모델을 생성하고 실행하는 클래스
FaceLandmarker = mp.tasks.vision.FaceLandmarker
# 얼굴 분석 옵션을 설정하는 클래스
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
# 모델 실행 방식을 VIDEO로 지정
VisionRunningMode = mp.tasks.vision.RunningMode

# 모델 설정
options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="./models/face_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=1,
    output_face_blendshapes=True,
)

landmarker = FaceLandmarker.create_from_options(options)

EYE_CLOSED_MIN = 0.45      # 눈 감김 판정 값
SLEEP_LIMIT_SEC = 0.3      # 졸음 판정 시간
eyes_closed_time = None   # 눈 감은 시작 시간

LEFT_EYE = [362, 263, 386, 374]
RIGHT_EYE = [33, 133, 159, 145]

cnt = 0
sleep_counted = False

# 졸음 발생 시간 기록
start_time = time.monotonic()
sleep_events = []


# 눈 영역 시각화
def draw_eye(image, landmarks, eye_indices, score, color):
    height, width = image.shape[:2]

    posX = []
    posY = []

    for i in eye_indices:
        posX.append(int(landmarks[i].x * width))
        posY.append(int(landmarks[i].y * height))

    # 사각형 좌표
    x1 = min(posX) - 5
    y1 = min(posY) - 5
    x2 = max(posX) + 5
    y2 = max(posY) + 5

    # 눈 주변 사각형
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)

    # 눈 감김 점수
    cv2.putText(
        image, f"{score:.2f}",
        (x1, y1 - 5), 0, 0.5, color, 1
    )


# 카메라에서 받은 이미지 분석
def analyze(image):
    global eyes_closed_time, cnt, sleep_counted

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_image
    )

    timestamp_ms = int(time.monotonic() * 1000)

    # 얼굴 분석
    result = landmarker.detect_for_video(mp_image, timestamp_ms)

    # 얼굴이 검출되지 않은 경우
    if not result.face_blendshapes:
        eyes_closed_time = None
        return None, None, "NO_FACE", 0.0, cnt

    # 첫 번째 얼굴
    blendshapes = result.face_blendshapes[0]

    left = None
    right = None

    for item in blendshapes:
        if item.category_name == "eyeBlinkLeft":
            left = item.score
        elif item.category_name == "eyeBlinkRight":
            right = item.score

    # 양쪽 눈의 점수가 기준값 이상이면 눈 감김
    eyes_closed = left >= EYE_CLOSED_MIN and right >= EYE_CLOSED_MIN

    now = time.monotonic()
    duration = 0.0

    if eyes_closed:
        if eyes_closed_time is None:
            eyes_closed_time = now

        duration = now - eyes_closed_time

        if duration >= SLEEP_LIMIT_SEC:
            status = "SLEEP"

            # 한 번의 졸음에 한 번만 카운트
            if not sleep_counted:
                cnt += 1
                sleep_counted = True
                sleep_events.append(now)

        else:
            status = "CLOSED"

    else:
        eyes_closed_time = None
        sleep_counted = False
        status = "NORMAL"

    landmarks = result.face_landmarks[0]

    # 졸음 판정 시간 대비 눈 감김 지속 시간 비율
    ratio = min(duration / SLEEP_LIMIT_SEC, 1.0)

    # 눈 감김 시간에 따라 초록색에서 빨간색으로 변화
    color = (0, int(255 * (1 - ratio)), int(255 * ratio))

    draw_eye(image, landmarks, LEFT_EYE, left, color)
    draw_eye(image, landmarks, RIGHT_EYE, right, color)

    return left, right, status, duration, cnt


# MediaPipe 모델 자원 해제
def close():
    landmarker.close()
