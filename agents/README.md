## Usage

```bash
docker compose up -d
docker exec -it ollama ollama pull dolphin3 # or qwen2.5:3b | dolphin3:8b
docker exec -it agents-agent-1 pip install requests psycopg2-binary
docker exec -it agents-agent-1 python agent.py
```