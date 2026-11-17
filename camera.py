import cv2
import vision

camera = cv2.VideoCapture(0, cv2.CAP_V4L)

# 프레임 크기 640*480
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# FPS 30으로 촬영 설정
camera.set(cv2.CAP_PROP_FPS, 30)

fourcc = cv2.VideoWriter_fourcc(*'DIVX') # 코덱 지정
writer = cv2.VideoWriter("video_4_4.avi", fourcc, 30, (640, 480)) # 30 프레임으로 객체 생성

while True:
    ret, image = camera.read()
    if ret == True:
        left, right, status, duration = vision.analyze(image)
        if left != None:
            print(f"Left: {left:.2f}, Right: {right:.2f}, Status: {status}, Time: {duration:.1f}s")
        else:
            print("얼굴 없음")

        cv2.imshow('preview', image)
        writer.write(image)    
    else:
        print('캡쳐 실패')
        break
    
    key = cv2.waitKey(1)
    if key == 115: # s누르면 이미지 캡쳐
        cv2.imwrite('test.jpg', image)
    elif key == 27: # ESC 누르면 종료
        break
writer.release()
camera.release()
cv2.destroyAllWindows()
vision.close()
