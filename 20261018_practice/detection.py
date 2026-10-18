import cv2
import numpy as np
pipeline = (
    "v4l2src device=/dev/video0 ! "
    "video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! "
    "videoconvert ! video/x-raw,format=BGR ! "
    "queue leaky=downstream max-size-buffers=1 "
    "max-size-bytes=0 max-size-time=0 ! "
    "appsink drop=true max-buffers=1 sync=false"
)

# TODO: 배운 기술(이미지 전처리, 특징 추출)을 활용하여 실시간으로 객체를 검출

# 초록 LAB lower/upper range
green_lower = np.array([30, 60, 90], dtype=np.uint8)
green_upper = np.array([230, 115, 180], dtype=np.uint8)

# cap = cv2.VideoCapture(0)

cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

while True:
    ret, frame = cap.read()

    if not ret:
        break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # 이진마스크 생성 (색상기반 분할)
    mask= cv2.cvtColor(mask, cv2.COLOR_2)
    mask = cv2.inRange(mask, green_lower, green_upper)
    # 마스크로 컨투어 검출
    contours, _ = cv2.findContours(
    mask,        # binary mask
    cv2.RETR_EXTERNAL,       # 구멍 뚫린 객체의 바깥쪽 테두리만 검출
    cv2.CHAIN_APPROX_SIMPLE  # 직선 경로 위에 있는 픽셀 좌표 전체 대신 꼭짓점 좌표만 저장
    )
    # 컨투어 중심 찾아서 원 그리기
    if len(contours) > 0:
        mask_color = np.zeros_like(final_img)
        mask_color[:, :, 1] = mask
        alpha = 0.35
        final_img = cv2.addWeighted(final_img, 1.0, mask_color, alpha, 0)

    cv2.drawContours(final_img, contours, -1, (255,0,0), 2)

    cv2.imshow("VideoCapture", frame)

# TODO: 각 프레임 이미지를 전처리
# TODO: Color Segmentation으로 Binary Mask 생s성
# TODO: 객체의 중심과 반지름을 구해 프레임 위에 overlay

cap.release()
cv2.destroyAllWindows()
