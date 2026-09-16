
**Terça, 30 ago** — O que fiz:

- Setup completo do ambiente (Homebrew, Git, Docker, Python, VS Code, Tailscale ligado à rede bridgelk.com)
- Estrutura inicial do repositório criada
- Ainda sem acesso ao BLKBosAI/Gitea 
- Corri o yolov8n no Mac, e passou-me automaticamente para a câmara do iPhone onde detetou poucos objetos corretamente por ser o modelo nano. Atenção que quando corro com a câmara do iPhone tenho de parar o programa no PC e não desligar no telemóvel.
- Testei o yolov8n sobre um vídeo próprio (model/videos/teste.mp4, 400 frames). Abriu, correu, fechou sozinho no fim. Latência por frame ~19-25ms (CPU, Mac). Detetou as pessoas identificando "person", mas além disso erou tudo (disse que uma tenda era "umbrella").
- Exportei o yolov8n.pt para ONNX usando model.export(format="onnx"). Sucesso em 6.4s, gerou yolov8n.onnx (12.3MB, maior que o .pt original de 6.2MB porque inclui a estrutura do grafo). Próximo passo: correr o modelo .onnx diretamente com onnxruntime (sem passar pelo ultralytics).

**Quarta, 31 ago** — O que fiz:

- Implementei o pipeline de inferência ONNX "à mão" (sem ultralytics): pré-processamento (letterbox + normalização + reordenação de eixos), inferência com onnxruntime (CPUExecutionProvider), e pós-processamento (decode das 8400 previsões + NMS via cv2.dnn.NMSBoxes).
- Testado no primeiro frame de model/videos/teste.mp4: encontrou 2 deteções ("umbrella" 0.78 e 0.64).
- Mesmo erro que ontem com a ultralytics (a tenda identificada como "umbrella", em vez de erro novo) — bom sinal, confirma que o pipeline manual está correto e a reproduzir o comportamento do modelo, não a introduzir bugs.
- R2 fechado: modelo YOLO a correr em runtime diferente do treino (onnxruntime vs PyTorch/ultralytics).
- Medi latência/débito do pipeline ONNX manual sobre os 400 frames do vídeo de teste: média 20.22ms, min 18.66ms, max 37.81ms, ~49.5 FPS (CPU, Mac). Consistente com os números da ultralytics de ontem.
- Defini a estrutura da mensagem de deteção (frame_id, timestamp, lista de deteções) e serializei em JSON. Payload de teste com 2 deteções: 253 bytes. Este número fica como baseline para comparar com Protobuf mais tarde.
- Corrigido o "No route to host" fixando IP_MULTICAST_IF="192.168.1.97" (rede Wi-Fi local) no publisher, para não depender da escolha automática de interface (Tailscale competia como candidata). Publisher e dois consumers a funcionar de forma reprodutível à primeira tentativa.