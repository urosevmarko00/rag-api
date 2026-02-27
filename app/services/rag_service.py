from app.models import models


class RAGService:

    def __init__(self, embedding_service, vector_store, chunking_service):
        self.model_name = "dummy_llm"
        self.embedding = embedding_service
        self.vector_store = vector_store
        self.chunking = chunking_service

    def ask(self, question: str) -> dict:
        if not question.strip():
            raise ValueError("Question cannot be empty or whitespace")

        query_embedding = self.embedding.embed(question)
        results = self.vector_store.search(query_embedding)

        if not results:
            context = ""
            answer = "No documents available yet."
        else:
            context = "\n".join([text for _, text in results])
            answer = f"[{self.model_name}]\nContext:\n {context}\n\n Question:\n{question}"

        return {
            "question": question,
            "context": context,
            "answer": answer
        }

    def add_document(self, document: models.Document):
        chunks = self.chunking.chunk(document.content)

        for chunk in chunks:
            self.vector_store.add(chunk, self.embedding.embed(chunk))
