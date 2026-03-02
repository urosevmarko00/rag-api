from app.models import models
import hashlib


class RAGService:

    def __init__(self, embedding_service, vector_store, chunking_service):
        self.model_name = "dummy_llm"
        self.embedding = embedding_service
        self.vector_store = vector_store
        self.chunking = chunking_service

    def ask(self, question: str, top_k: int = 3) -> dict:
        if not question.strip():
            raise ValueError("Question cannot be empty or whitespace")

        query_embedding = self.embedding.embed(question)
        results = self.vector_store.search(query_embedding, top_k)

        if not results:
            context = ""
            answer = "No documents available yet."
        else:
            context = "\n".join([text for _, _, _, text in results])
            answer = f"[{self.model_name}]\nContext:\n {context}\n\n Question:\n{question}"

        return {
            "question": question,
            "context": context,
            "retrieved_chunks": [{"doc_id": doc_id,
                                  "score": score,
                                  "title": title,
                                  "text": text} for score, doc_id, title, text in results],
            "answer": answer
        }

    def add_document(self, document: models.Document):
        doc_identity_string = document.title + "::" + document.content
        doc_id = hashlib.sha256(doc_identity_string.encode()).hexdigest()
        if self.vector_store.document_exists(doc_id):
            raise ValueError("Document already exists")

        chunks = self.chunking.chunk(document.content)

        for chunk in chunks:
            self.vector_store.add(doc_id, document.title, chunk, self.embedding.embed(chunk))

        self.vector_store.save()
