from app.models import models
import hashlib
from app.core.logger import get_logger
import time

logger = get_logger(__name__)


class RAGService:

    def __init__(self, embedding_service, vector_store, chunking_service, llm):
        self.embedding = embedding_service
        self.vector_store = vector_store
        self.chunking = chunking_service
        self.llm = llm

    def ask(self, question: str, top_k: int = 3) -> dict:
        if not question.strip():
            raise ValueError("Question cannot be empty or whitespace")

        logger.info(f"Received question: {question}")

        query_embedding = self.embedding.embed(question)

        start_search = time.time()
        results = self.vector_store.search(query_embedding, top_k)
        search_time = time.time() - start_search

        logger.info(f"Retrieved {len(results)} chunks in {search_time:.2f}s")

        if not results:
            logger.warning("No documents available for retrieval")
            context = ""
            answer = "No documents available yet."
        else:
            context = "\n".join([text for _, _, _, text in results])

            start_llm = time.time()
            answer = self.llm.generate(context, question)
            llm_time = time.time() - start_llm

            logger.info(f"LLM response generated in {llm_time:.3f}s")

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
        logger.info(f"Adding document {document.title}")

        doc_identity_string = document.title + "::" + document.content
        doc_id = hashlib.sha256(doc_identity_string.encode()).hexdigest()

        if self.vector_store.document_exists(doc_id):
            logger.warning("Attempt to add duplicate document")
            raise ValueError("Document already exists")

        chunks = self.chunking.chunk(document.content)
        logger.info(f"Document split into {len(chunks)} chunks")

        for chunk in chunks:
            self.vector_store.add(doc_id, document.title, chunk, self.embedding.embed(chunk))

        self.vector_store.save()
        logger.info("Document successfully added and indexed")
