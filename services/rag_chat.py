import requests

from services.vector_store import semantic_search

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """
You are a personal AI knowledge assistant.

Answer ONLY using the provided summaries.

If the information is not available in the summaries, clearly say:
"I could not find that information in your saved summaries."

Be concise, practical, and insightful.
"""


def build_context(results):
    documents = results["documents"][0]

    context = "\n\n---\n\n".join(documents)

    return context


def build_rag_prompt(question: str, context: str):
    return f"""
{SYSTEM_PROMPT}

Context summaries:
{context}

User question:
{question}

Answer:
"""


def ask_question(question: str):
    results = semantic_search(question, n_results=4)

    context = build_context(results)

    prompt = build_rag_prompt(question, context)

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

    return {
        "answer": data["response"],
        "sources": results["metadatas"][0]
    }
