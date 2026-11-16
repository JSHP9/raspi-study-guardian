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

# 얼굴 분석 모델 생성(종료시 자동 해제)
with FaceLandmarker.create_from_options(options) as landmarker:
    # 얼굴 분석 모델 생성
    landmarker = FaceLandmarker.create_from_options(options)

# 카메라에서 받은 이미지를 분석
def analyze(image):
    # OpenCV BGR 이미지를 RGB로 변환
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # MediaPipe 입력 형식으로 변환
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

    # 프레임 시간 생성
    timestamp_ms = int(time.monotonic() * 1000)

    # 얼굴 분석 후 검출된 얼굴 수 반환
    result = landmarker.detect_for_video(mp_image, timestamp_ms)
    return len(result.face_landmarks)

# MediaPipe 모델 자원 해제
def close():
    landmarker.close()
