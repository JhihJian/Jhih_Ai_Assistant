import cv2
from PIL import ImageEnhance
from PIL import Image

cap = cv2.VideoCapture(0)
f, frame = cap.read()  # 此刻拍照
cv2.imwrite("example.png", frame)  # 将拍摄内容保存为png图片
cap.release()  # 关闭调用的摄像头

image = Image.open("example.png")
enh_bri = ImageEnhance.Brightness(image)
brighted_image = enh_bri.enhance(2)
brighted_image.show()
