from ultralytics import YOLO
import cv2

cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv2.VideoWriter('output.avi', cv2.VideoWriter.fourcc(), 30, (frame_width, frame_height))

model = YOLO('../Yolo-Weights/yolov8n.pt')
while True:
    success, img = cap.read()
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('1'):
        break
out.release()
