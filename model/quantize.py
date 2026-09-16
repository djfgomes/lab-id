from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic(
    model_input="model/yolov8n_prep.onnx",
    model_output="model/yolov8n_int8.onnx",
    weight_type=QuantType.QUInt8,
)

print("Modelo quantizado guardado em model/yolov8n_int8.onnx")