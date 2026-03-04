# Mini RAG API

A production-style Retrieval-Augmented Generation (RAG) backend built with FastAPI, FAISS, and pluggable LLM providers.

The system supports local and OpenAI-based language models, persistent vector storage, and Dockerized network deployment.

---
## Project goal
This project demonstrates:
+ End-to-end RAG pipeline implementation
+ Vector similarity search using FAISS
+ Pluggable LLM architecture (local + OpenAI)
+ Dockerized backend deployment
+ Persistent vector storage using volumes
+ Network-accessible API

---
## Features

+ Smart sliding-window chunking with overlap
+ FAISS vector similarity search
+ Sentence-Transformers embeddings
+ Pluggable LLM abstraction (BaseLLM → LocalLLM / OpenAI)
+ Structured logging with latency tracking
+ Dockerized deployment
+ Persistent FAISS index via Docker volumes
+ Accessible from other machines in local network

---
## Tech Stack

+ FastAPI
+ FAISS (vector similarity search)
+ Sentence-Transformers
+ OpenAI API (optional)
+ Requests
+ Docker

---
## Architecture

1. Documents are chunked using sliding window strategy.
2. Chunks are embedded using Sentence Transformers.
3. Embeddings are stored in FAISS index.
4. User query is embedded.
5. Top-k relevant chunks are retrieved.
6. Retrieved context is passed to selected LLM provider.
7. Final response is returned via FastAPI.

---
## Configuration
| Variable                  | Description              |
|---------------------------|--------------------------|
| LLM_PROVIDER              | `local` or `openai`      |
| OPENAI_API_KEY            | Required if using OpenAI |

Example `.env`:
```
LLM_PROVIDER=local
```
---
## Running Locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Access Swagger:
```
http://localhost:8000/docs
```
---
## Running with Docker

### Build
```bash
docker build -t mini-rag-api .
```
### Run with persistent storage
Linux / MAC:
```bash
docker run -d \
  --name mini-rag-api-container \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  mini-rag-api
```
Windows PowerShell:
```powershell
docker run -d `
  --name mini-rag-api-container `
  -p 8000:8000 `
  --env-file .env `
  -v ${PWD}/data:/app/data `
  mini-rag-api
```
---
## Access from another machine
If host machine IP is:
```
192.168.0.10
```
Access API via:
```
http://192.168.0.10:8000/docs
```
Ensure firewall allows port 8000

---
## API Endpoints

+ POST /documents → Add document
+ POST /ask → Ask question

---
## Logging

Includes:

+ Search latency measurement
+ LLM generation latency
+ FAISS load/save logs
+ Request-level tracing

---
## Future Improvements

+ Hybrid search (BM25 + vector)
+ Streaming LLM responses
+ Authentication & rate limiting
+ Docker Compose setup
+ Kubernetes deployment

---
## Author
Marko Urošev