
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 1. MediaPipe 손 인식 모델 설정
base_options = python.BaseOptions(
    model_asset_path="src/models/MediaPipe/hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)


# 2. 카메라 설정 (수업 파이프라인)
pipeline = (
    "v4l2src device=/dev/video0 ! "
    "video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! "
    "videoconvert ! video/x-raw,format=BGR ! "
    "queue leaky=downstream max-size-buffers=1 "
    "max-size-bytes=0 max-size-time=0 ! "
    "appsink drop=true max-buffers=1 sync=false"
)

cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Camera open failed")
    detector.close()
    raise SystemExit


# 3. 가상 공 초기 설정
ball_x, ball_y = 320, 240
radius = 30
grabbed = False


# 4. 실시간 영상 처리
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # 좌우 반전
    frame = cv2.flip(frame, 1)

    # 영상 크기
    h, w = frame.shape[:2]

    # BGR -> RGB 변환
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # MediaPipe 손 인식
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)

    # 5. 손이 인식된 경우
    if result.hand_landmarks:
        hand = result.hand_landmarks[0]

        # 엄지 끝(4번)
        tx = int(hand[4].x * w)
        ty = int(hand[4].y * h)

        # 검지 끝(8번)
        ix = int(hand[8].x * w)
        iy = int(hand[8].y * h)

        # 두 손가락의 중간 좌표
        cx = (tx + ix) // 2
        cy = (ty + iy) // 2

        # 엄지와 검지 사이 거리
        distance = np.hypot(tx - ix, ty - iy)

        # 손가락 중간점과 공 사이 거리
        ball_distance = np.hypot(
            cx - ball_x, cy - ball_y
        )

        # 6. 공 잡기
        if not grabbed and distance < 35 and ball_distance < 55:
            grabbed = True

        # 7. 공 놓기
        if grabbed and distance > 55:
            grabbed = False

        # 8. 공 이동
        if grabbed:
            ball_x, ball_y = cx, cy

        # 손가락 위치 표시
        cv2.circle(frame, (tx, ty), 7, (255, 0, 0), -1)
        cv2.circle(frame, (ix, iy), 7, (255, 0, 0), -1)

        # 두 손가락 연결
        cv2.line(
            frame, (tx, ty), (ix, iy),
            (0, 255, 0), 2
        )

    else:
        grabbed = False

    # 9. 가상 공 그리기
    cv2.circle(
        frame,
        (ball_x, ball_y),
        radius,
        (0, 140, 255),
        -1
    )

    # 10. 상태 표시
    if grabbed:
        status = "GRABBED"
        color = (0, 255, 0)
    else:
        status = "RELEASED"
        color = (0, 0, 255)

    cv2.putText(
        frame, status, (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1, color, 2
    )

    # 화면 출력
    cv2.imshow("Virtual Ball Control", frame)

    # q를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# 11. 종료
cap.release()
detector.close()
cv2.destroyAllWindows()
