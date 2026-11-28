import cv2
import vision
import buzzer

def generate_frame():
    camera = cv2.VideoCapture(0, cv2.CAP_V4L)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, 30)

    try:
        while True:
            ret, image = camera.read()

            if not ret:
                break

            left, right, status, duration, sleep_cnt = vision.analyze(image)

            # 알람
            buzzer.alert(status, sleep_cnt)

            # 누적 졸음 횟수 출력
            cv2.putText(
                image, f"sleep Count: {sleep_cnt}",
                (20, 40), 0, 0.8, (255, 255, 255), 2
            )

            # png로 인코딩
            success, buffer = cv2.imencode(".png", image)

            if not success:
                continue

            # 프레임 전송
            yield (
                b"--frame\r\n"
                b"Content-Type: image/png\r\n\r\n"
                + buffer.tobytes() + b"\r\n"
            )

    finally:
        camera.release()
        buzzer.alert("NORMAL", 0)
        vision.eyes_closed_time = None
