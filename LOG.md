## Semana 1 (30 ago – 1 set)

**Terça, 30 ago** — O que fiz:

- Setup completo do ambiente (Homebrew, Git, Docker, Python, VS Code, Tailscale ligado à rede bridgelk.com)
- Estrutura inicial do repositório criada
- Ainda sem acesso ao BLKBosAI/Gitea 
- Corri o yolov8n no Mac, e passou-me automaticamente para a câmara do iPhone onde detetou poucos objetos corretamente por ser o modelo nano. Atenção que quando corro com a câmara do iPhone tenho de parar o programa no PC e não desligar no telemóvel.
- Testei o yolov8n sobre um vídeo próprio (model/videos/teste.mp4, 400 frames). Abriu, correu, fechou sozinho no fim. Latência por frame ~19-25ms (CPU, Mac). Detetou as pessoas identificando "person", mas além disso erou tudo (disse que uma tenda era "umbrella").
- Exportei o yolov8n.pt para ONNX usando model.export(format="onnx"). Sucesso em 6.4s, gerou yolov8n.onnx (12.3MB, maior que o .pt original de 6.2MB porque inclui a estrutura do grafo). Próximo passo: correr o modelo .onnx diretamente com onnxruntime (sem passar pelo ultralytics).