import json
import time


def build_message(frame_id, detections):
    return {
        "frame_id": frame_id,
        "timestamp": time.time(),
        "detections": [
            {
                "class": d["class"],
                "confidence": round(float(d["confidence"]), 3),
                "x1": round(float(d["x1"]), 1),
                "y1": round(float(d["y1"]), 1),
                "x2": round(float(d["x2"]), 1),
                "y2": round(float(d["y2"]), 1),
            }
            for d in detections
        ],
    }


def to_json_bytes(message):
    """Serializa a mensagem para JSON, devolve bytes (o que vai para a rede)."""
    return json.dumps(message).encode("utf-8")

if __name__ == "__main__":
    fake_detections = [
        {"class": "person", "confidence": 0.87, "x1": 100.0, "y1": 200.0, "x2": 300.0, "y2": 500.0},
        {"class": "umbrella", "confidence": 0.78, "x1": 519.0, "y1": 628.0, "x2": 1079.0, "y2": 1584.0},
    ]
    message = build_message(frame_id=0, detections=fake_detections)
    payload = to_json_bytes(message)

    print(message)
    print(f"Tamanho do payload: {len(payload)} bytes")