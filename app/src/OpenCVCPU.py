import cv2
import numpy as np
import os

# 애니메이션 생성
output_path = "circle_animation.mp4"
width, height, fps = 512, 512, 30
writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

for r in list(np.linspace(20, 100, 30)) + list(np.linspace(100, 20, 30)):
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (255, 0, 0)
    cv2.circle(img, (width//2, height//2), int(r), (255, 255, 255), -1)
    writer.write(img)

writer.release()
print("🎞️ 동영상 저장 완료:", output_path)

# 자동 재생 (Windows 전용)
os.startfile(output_path)
