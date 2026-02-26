class RAGService:

    def __init__(self):
        self.model_name = "dummy_llm"

    def ask(self, question: str) -> dict:
        if not question.strip():
            raise ValueError("Question cannot be empty or whitespace")
        context = "Fake context"
        answer = f"[{self.model_name}] {question}"

        return {
            "question": question,
            "context": context,
            "answer": answer
        }
