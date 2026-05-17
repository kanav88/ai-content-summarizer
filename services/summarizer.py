import requests
from prompts import build_summary_prompt

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


def summarize_content(content: str, tone: str, output_type: str) -> str:
    prompt = build_summary_prompt(content, tone, output_type)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()
    data = response.json()

    return data["response"]