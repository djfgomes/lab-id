import csv

with open("model/latencia_onnx.csv") as f:
    reader = csv.DictReader(f)
    latencies = [float(row["latencia_ms"]) for row in reader]

media = sum(latencies) / len(latencies)
minimo = min(latencies)
maximo = max(latencies)
fps = 1000 / media  # débito: frames por segundo

print(f"Frames processados: {len(latencies)}")
print(f"Latência média: {media:.2f} ms")
print(f"Latência mínima: {minimo:.2f} ms")
print(f"Latência máxima: {maximo:.2f} ms")
print(f"Débito estimado: {fps:.1f} FPS")