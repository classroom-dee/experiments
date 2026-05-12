## Usage

```bash
docker compose up -d
docker exec -it ollama ollama pull qwen2.5:3b # or dolphin3 | dolphin3:8b
docker exec -it agents-agent-1 pip install requests
docker exec -it agents-agent-1 python agent.py
```