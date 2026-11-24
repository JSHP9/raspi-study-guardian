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

# 모델 설정(파일 경로, 영상 모드, 얼굴 수, 표정 점수 반환)
options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="./models/face_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=1,
    output_face_blendshapes=True,
)

# 얼굴 분석 모델 생성
landmarker = FaceLandmarker.create_from_options(options)

EYE_CLOSED_MIN = 0.45        # 눈 떴다고 보는 최소 기준값
SLEEP_LIMIT_SEC = 1.5      # 졸음으로 판단하는 시간
eyes_closed_time = None    # 눈 감기 시작한 시간


# 카메라에서 받은 이미지를 분석
def analyze(image):
    global eyes_closed_time

    # OpenCV BGR 이미지를 RGB로 변환
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # MediaPipe 입력 형식으로 변환
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

    # 프레임 시간 생성
    timestamp_ms = int(time.monotonic() * 1000)

    # 얼굴 분석 후 검출된 얼굴 수 반환
    result = landmarker.detect_for_video(mp_image, timestamp_ms)
    
    # 얼굴 안보이는 경우  전부 초기화
    if not result.face_blendshapes:
        eyes_closed_time = None
        return None, None, "NO_FACE", 0.0 

    # 첫번째 얼굴
    blendshapes = result.face_blendshapes[0]

    left = None
    right = None

    for item in blendshapes:
        if item.category_name == "eyeBlinkLeft": # 왼쪽 눈
            left = item.score
        elif item.category_name == "eyeBlinkRight": # 오른쪽 눈
            right = item.score

    # 양쪽눈이 전부 최소 점수 이상이면 눈 감은거
    eyes_closed = left >= EYE_CLOSED_MIN and right >= EYE_CLOSED_MIN

    now = time.monotonic()
    duration = 0.0

    if eyes_closed: # 눈 감음
        if eyes_closed_time is None:
            eyes_closed_time = now

        duration = now - eyes_closed_time

        if duration >= SLEEP_LIMIT_SEC:
            status = "SLEEP"
        else:
            status = "CLOSED"
    else: # 눈 뜸
        eyes_closed_time = None
        status = "NORMAL"


    # 양쪽 눈 리턴
    return left, right, status, duration

# MediaPipe 모델 자원 해제
def close():
    landmarker.close()
