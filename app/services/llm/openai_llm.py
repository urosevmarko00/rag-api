from openai import OpenAI
import os
from app.services.llm.base_llm import BaseLLM


class OpenAILLM(BaseLLM):

    def __init__(self, model_name: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")

        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def generate(self, context: str, question: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "Answer strictly based on provided context. "
                               "If answer is not in context say you don't know."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion:\n{question}"
                }
            ],
            temperature=0.2,
            max_tokens=500
        )

        return response.choices[0].message.content
