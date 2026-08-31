import cv2
import numpy as np
import onnxruntime as ort
import time
import csv
from serialize import build_message, to_json_bytes
from udp_publisher import create_publisher_socket, publish

COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
    "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush"
]


def preprocess(frame, input_size=640):
    h, w = frame.shape[:2]
    scale = input_size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)

    resized = cv2.resize(frame, (new_w, new_h))

    padded = np.full((input_size, input_size, 3), 114, dtype=np.uint8)
    padded[0:new_h, 0:new_w] = resized

    img = padded[:, :, ::-1].transpose(2, 0, 1).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    return img, scale


def load_model(onnx_path):
    session = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
    return session


def infer(session, img):
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: img})
    return outputs[0]


def postprocess(output, scale, conf_threshold=0.25, iou_threshold=0.45):
    predictions = output[0].T

    boxes = predictions[:, :4]
    class_scores = predictions[:, 4:]

    class_ids = np.argmax(class_scores, axis=1)
    confidences = np.max(class_scores, axis=1)

    mask = confidences >= conf_threshold
    boxes = boxes[mask]
    confidences = confidences[mask]
    class_ids = class_ids[mask]

    if len(boxes) == 0:
        return []

    x1 = boxes[:, 0] - boxes[:, 2] / 2
    y1 = boxes[:, 1] - boxes[:, 3] / 2
    w = boxes[:, 2]
    h = boxes[:, 3]
    boxes_xywh = np.column_stack([x1, y1, w, h])

    indices = cv2.dnn.NMSBoxes(
        boxes_xywh.tolist(), confidences.tolist(), conf_threshold, iou_threshold
    )

    detections = []
    for i in indices:
        i = int(i)
        bx1, by1, bw, bh = boxes_xywh[i]
        detections.append({
            "class": COCO_CLASSES[class_ids[i]],
            "confidence": float(confidences[i]),
            "x1": bx1 / scale,
            "y1": by1 / scale,
            "x2": (bx1 + bw) / scale,
            "y2": (by1 + bh) / scale,
        })

    return detections


def draw_detections(frame, detections):
    """Desenha as caixas e etiquetas por cima do frame original."""
    for d in detections:
        x1, y1, x2, y2 = int(d["x1"]), int(d["y1"]), int(d["x2"]), int(d["y2"])
        label = f"{d['class']} {d['confidence']:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, max(y1 - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return frame


if __name__ == "__main__":
    session = load_model("model/yolov8n.onnx")
    cap = cv2.VideoCapture("model/videos/teste.mp4")

    csv_file = open("model/latencia_onnx.csv", "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["frame", "latencia_ms"])

    pub_socket = create_publisher_socket(interface_ip="192.168.1.97")

    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        start = time.perf_counter()

        img, scale = preprocess(frame)
        output = infer(session, img)
        detections = postprocess(output, scale)

        end = time.perf_counter()
        latency_ms = (end - start) * 1000
        csv_writer.writerow([frame_num, f"{latency_ms:.2f}"])

        message = build_message(frame_id=frame_num, detections=detections)
        payload = to_json_bytes(message)

        publish(pub_socket, payload)

        if frame_num % 50 == 0:
            print(f"Frame {frame_num}: {len(detections)} deteções, payload {len(payload)} bytes (enviado)")
            
        frame = draw_detections(frame, detections)
        cv2.imshow("Deteccoes ONNX", frame)

        frame_num += 1

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    pub_socket.close()
    csv_file.close()
    cap.release()
    cv2.destroyAllWindows()
    print(f"Terminado. {frame_num} frames processados. Latências guardadas em model/latencia_onnx.csv")