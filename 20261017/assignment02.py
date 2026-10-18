from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 농구공 이미지 불러오기
path = Path(__file__).resolve().parent.parent / "src/images/basketball_crop.jpg"
basketball = cv2.imread(str(path))

if basketball is None:
    raise FileNotFoundError("농구공 이미지 파일을 확인해주세요.")

basketball_rgb = cv2.cvtColor(basketball, cv2.COLOR_BGR2RGB)

# LAB 색공간으로 변환 후 CLAHE 적용
basketball_lab = cv2.cvtColor(basketball, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(basketball_lab)

clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
l_clahe_enhanced = clahe.apply(l)
basketball_enhanced_lab = cv2.merge((l_clahe_enhanced, a, b))

# 강화된 이미지로 binary mask 생성
lower_basketball_lab = np.array([70, 130, 70])
upper_basketball_lab = np.array([180, 230, 185])

mask_enhanced = cv2.inRange(
    basketball_enhanced_lab, lower_basketball_lab, upper_basketball_lab
)

# 강의 예제: Opening과 Closing 결과 비교
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

ball_mask_opened = cv2.morphologyEx(mask_enhanced, cv2.MORPH_OPEN, kernel)
ball_mask_closed = cv2.morphologyEx(mask_enhanced, cv2.MORPH_CLOSE, kernel)

plt.figure(figsize=(16, 8))
plt.subplot(1, 3, 1), plt.imshow(mask_enhanced, cmap="gray"), plt.title("Enhanced Mask")
plt.subplot(1, 3, 2), plt.imshow(ball_mask_opened, cmap="gray"), plt.title("Mask after Opening")
plt.subplot(1, 3, 3), plt.imshow(ball_mask_closed, cmap="gray"), plt.title("Mask after Closing")

for ax in plt.gcf().axes:
    ax.axis("off")

# TODO: Morphological operation을 적용하여 최종 binary mask 생성
final_ball_mask = cv2.morphologyEx(ball_mask_opened, cv2.MORPH_CLOSE, kernel)

# TODO: Binary mask로 외곽선 검출
contours, _ = cv2.findContours(
    final_ball_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

# TODO: 최종 농구공 영역 및 외곽선 선택
final_img = basketball_rgb.copy()

if len(contours) > 0:
    largest_contour = max(contours, key=cv2.contourArea)

    final_mask = np.zeros_like(final_ball_mask)
    cv2.drawContours(final_mask, [largest_contour], -1, 255, cv2.FILLED)

    mask_color = np.zeros_like(final_img)
    mask_color[:, :, 1] = final_mask
    final_img = cv2.addWeighted(final_img, 1.0, mask_color, 0.35, 0)

    cv2.drawContours(final_img, [largest_contour], -1, (0, 255, 0), 2)

plt.figure(figsize=(8, 8))
plt.imshow(final_img)
plt.title("Basketball Contour")
plt.axis("off")
plt.show()
