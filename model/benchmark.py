import sys
import time
import csv
import cv2

from quickstart_onnx import load_model, preprocess, infer, postprocess


def run_benchmark(model_path, video_path, output_csv):
    session = load_model(model_path)
    cap = cv2.VideoCapture(video_path)

    csv_file = open(output_csv, "w", newline="")
    writer = csv.writer(csv_file)
    writer.writerow(["frame", "latencia_ms", "num_deteccoes", "confianca_media"])

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
        num_det = len(detections)
        avg_conf = (sum(d["confidence"] for d in detections) / num_det) if num_det else 0.0

        writer.writerow([frame_num, f"{latency_ms:.2f}", num_det, f"{avg_conf:.3f}"])
        frame_num += 1

    cap.release()
    csv_file.close()
    print(f"{model_path}: {frame_num} frames -> {output_csv}")


if __name__ == "__main__":
    model_path = sys.argv[1]
    output_csv = sys.argv[2]
    run_benchmark(model_path, "model/videos/teste.mp4", output_csv)