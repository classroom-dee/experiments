import json
import os
import requests

from db import execute_query

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
- read_file(path)
- plain_text_response(message)
- execute_query(query)
"""

messages.append({"role": "system", "content": SYSTEM_PROMPT})


def list_files(path="."):
    return os.listdir(path)


def read_file(path="."):
    return open(path).read()


def plain_text_response(message):
    print("\nAgent:", message, "\n")


def execute_query_tool(query):
    return execute_query(query)


TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "plain_text_response": plain_text_response,
    "execute_query": execute_query_tool,
}


while True:
    user = input("You: ")

    messages.append({"role": "user", "content": user})

    r = requests.post(
        "http://ollama:11434/api/chat",
        json={"model": MODEL, "messages": messages, "stream": False},
    )

    content = r.json()["message"]["content"]

    try:
        tool_call = json.loads(content)

        tool_name = tool_call["tool"]
        args = tool_call["args"]

        result = TOOLS[tool_name](**args)

        tool_message = result if isinstance(result, str) else json.dumps(result)

        plain_text_response(tool_message)

        messages.append({"role": "assistant", "content": content})

        messages.append({"role": "tool", "content": tool_message})

    except Exception as e:
        plain_text_response(content, f"Error: {e}")

        messages.append({"role": "assistant", "content": content})
