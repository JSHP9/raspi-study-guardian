import cv2
import vision
import buzzer

def generate_frame():
    camera = cv2.VideoCapture(0, cv2.CAP_V4L)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, 30)

    try :
        while True:
            ret, image = camera.read()

            if not ret:
                break

            left, right, status, duration, sleep_cnt = vision.analyze(image)
        
            # 알람
            buzzer.alert(status, sleep_cnt)

            color = (0, 0, 255) if status == "SLEEP" else (0, 255, 0)
            # 졸음 상태
            cv2.putText( #이미지, 텍스트, 위치, 폰트, 크기, 색, 두께
                image, f"Status: {status} | Time: {duration:.1f}s",
                (20, 40), 0, 0.7, color, 1
            )

            # 좌우 눈 감김 점수
            if left is not None and right is not None:
                cv2.putText(
                    image,
                    f"Left: {left:.2f} | Right: {right:.2f}",
                    (20, 80), 0, 0.7, color, 1
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
