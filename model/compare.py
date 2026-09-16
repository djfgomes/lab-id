import csv


def stats(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    latencies = [float(r["latencia_ms"]) for r in rows]
    detections = [int(r["num_deteccoes"]) for r in rows]
    confidences = [float(r["confianca_media"]) for r in rows if int(r["num_deteccoes"]) > 0]

    media_lat = sum(latencies) / len(latencies)
    return {
        "n_frames": len(rows),
        "latencia_media_ms": media_lat,
        "latencia_min_ms": min(latencies),
        "latencia_max_ms": max(latencies),
        "fps": 1000 / media_lat,
        "deteccoes_media": sum(detections) / len(detections),
        "confianca_media": sum(confidences) / len(confidences) if confidences else 0.0,
    }


for label, path in [("FP32", "results/latencia_fp32.csv"), ("INT8", "results/latencia_int8.csv")]:
    s = stats(path)
    print(f"\n--- {label} ---")
    for k, v in s.items():
        print(f"{k}: {v:.3f}" if isinstance(v, float) else f"{k}: {v}")