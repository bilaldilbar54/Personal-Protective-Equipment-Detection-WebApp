from ultralytics import YOLO
import cv2
import math


def const_video_detection(path_x, label_scale=1.0, conf_scale=1.0):
    video_capture = path_x
    cap = cv2.VideoCapture(video_capture)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    model = YOLO("const-ppe-detector(3).pt")
    classNames = ['Protective Helmet', 'Shield', 'Jacket', 'Dust Mask', 'Eye Wear', 'Glove', 'Protective Boots']

    while True:
        success, img = cap.read()
        if not success:
            break

        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                label = f'{class_name}{conf}'

                # Scale the font size
                label_font_scale = label_scale
                conf_font_scale = conf_scale

                t_size_label = cv2.getTextSize(label, 0, fontScale=label_font_scale, thickness=2)[0]
                c2 = x1 + t_size_label[0], y1 - t_size_label[1] - 3
                if class_name == 'Protective Helmet':
                    color = (0, 204, 255)
                elif class_name == "Glove":
                    color = (222, 82, 175)
                elif class_name == "Dust Mask":
                    color = (0, 149, 255)
                else:
                    color = (85, 45, 255)

                if conf > 0.2:
                    # Draw bounding box
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                    cv2.rectangle(img, (x1, y1), c2, color, -1, cv2.LINE_AA)  # filled
                    # Draw label and confidence
                    cv2.putText(img, label, (x1, y1 - 2), 0, label_font_scale, [255, 255, 255], thickness=1,
                                lineType=cv2.LINE_AA)
                    cv2.putText(img, f'{conf}', (x1, y1 - int(t_size_label[1] * 1.5)), 0, conf_font_scale,
                                [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        yield img

    cap.release()


cv2.destroyAllWindows()
