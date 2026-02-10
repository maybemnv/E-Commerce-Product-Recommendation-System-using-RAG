# Design Decisions & Architecture

## 1. Core Architecture

The system is built as a lightweight, stateless microservice using **FastAPI** to orchestrate the RAG (Retrieval-Augmented Generation) pipeline.

### Components

- **API Layer (FastAPI)**: Handles request/response validation, file uploads, and error handling. Chosen for its native asynchronous capabilities and automatic OpenAPI documentation.
- **Vector Store (ChromaDB)**: An embedded vector database running locally.
  - _Rationale_: ChromaDB requires no external server process (unlike PostgreSQL/pgvector or Elasticsearch), allowing this project to be "clone-and-run" compatible.
- **LLM Provider (Google Gemini)**: Used for the generation phase.
  - _Rationale_: Gemini offers a generous free tier and large context window (1M+ tokens), making it superior for development and testing compared to OpenAI's strictly metered availability.

## 2. RAG Pipeline Implementation

The pipeline follows a standard "Retrieve-Then-Generate" flow:

1.  **Ingestion & Chunking**:
    - Files (PDF, TXT, DOCX) are parsed into raw text.
    - **Strategy**: Text is split into **500-word chunks** with a **50-word overlap**.
    - _Why?_ 500 words provide enough context for the LLM to answer complex questions, while the overlap prevents information loss at chunk boundaries.

2.  **Embedding**:
    - We use the `sentence-transformers/all-MiniLM-L6-v2` model locally.
    - _Why?_ Using a local embedding model eliminates API costs and latency for the vectorization step. The model is small (~80MB) and runs efficiently on standard CPUs.

3.  **Retrieval**:
    - Queries are embedded using the same model.
    - ChromaDB performs a standard **Cosine Similarity** search to find the top 5 most relevant chunks.

4.  **Generation**:
    - A strict system prompt is constructed combining the User Query + Retrieved Context.
    - The LLM is instructed to answer _strictly_ based on the context to minimize hallucinations.

## 3. Trade-offs & Limitations

- **Local Persistence**: Vector data is stored in the `./data` directory. This is not suitable for horizontal scaling (multiple API instances cannot reliably share the same SQLite-backed Chroma file).
- **Synchronous Processing**: Large file uploads block the request thread until processing is complete. A production version would use background tasks (Celery/Redis).

## 4. Future Roadmap

To move this system to production, the following improvements are recommended:

1.  **Containerization**: Dockerize the application for consistent deployment.
2.  **Remote Vector Store**: Migrate ChromaDB to Client/Server mode or use a cloud provider (Pinecone/Weaviate).
3.  **Authentication**: Add API Key or OAuth2 protection to endpoints.
4.  **Async Ingestion**: Offload document processing to a background worker queue.
