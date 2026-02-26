class RAGService:

    def __init__(self):
        self.model_name = "dummy_llm"

    def ask(self, question: str) -> dict:
        context = "Fake context"
        answer = f"[{self.model_name}] {question}"

        return {
            "question": question,
            "context": context,
            "answer": answer
        }
