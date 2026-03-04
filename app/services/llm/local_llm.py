import requests
from app.services.llm.base_llm import BaseLLM


class LocalLLM(BaseLLM):

    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.url = "http://host.docker.internal:11434/api/generate"

    def generate(self, context: str, question: str) -> str:
        prompt = f"""
Answer strictly based on the context.
If answer is not in context say you don't know.

Context:
{context}

Question:
{question}
"""
        response = requests.post(
            self.url,
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"]
