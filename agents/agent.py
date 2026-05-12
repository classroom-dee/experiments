import json
import os
import requests

# MODEL = "qwen2.5:3b"
MODEL = "dolphin3"

messages = []

SYSTEM_PROMPT = """
You are an agent.

If you need to use a tool, respond ONLY in JSON.

Example:

{
  "tool": "list_files",
  "args": {
    "path": "."
  }
}

Available tools:
- list_files(path)
"""

messages.append({
    "role": "system",
    "content": SYSTEM_PROMPT
})


def list_files(path="."):
    return os.listdir(path)

def read_file(path="."):
    return open(path).read()

def print_message(message):
    print("\nAgent:", message, "\n")


TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "print_message": print_message
}


while True:
    user = input("You: ")

    messages.append({
        "role": "user",
        "content": user
    })

    r = requests.post(
        "http://ollama:11434/api/chat",
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False
        }
    )

    content = r.json()["message"]["content"]

    try:
        tool_call = json.loads(content)

        tool_name = tool_call["tool"]
        args = tool_call["args"]

        result = TOOLS[tool_name](**args)

        tool_message = f"TOOL RESULT: {result}"

        print_message(tool_message)

        messages.append({
            "role": "assistant",
            "content": content
        })

        messages.append({
            "role": "user",
            "content": tool_message
        })

    except Exception:
        print_message(content)

        messages.append({
            "role": "assistant",
            "content": content
        })