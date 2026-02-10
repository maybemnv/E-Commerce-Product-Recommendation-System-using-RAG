# Design Architecture & Decisions

## 1. System Architecture

The recommendation system utilizes a **Retrieval-Augmented Generation (RAG)** pipeline orchestrated via a stateless microservice. The architecture prioritizes local execution for the retrieval phase to minimize latency and operational complexity, while leveraging cloud-based LLMs for high-quality generation.

### Core Components

- **FastAPI (Application Layer)**: Selected for its asynchronous request handling and native Pydantic integration, ensuring strict type safety and high throughput for concurrent requests.
- **ChromaDB (Vector Store)**: Implemented as an embedded vector database. This design choice eliminates the need for external database infrastructure (e.g., PostgreSQL/Elasticsearch), facilitating rapid deployment and simplifying the development environment.
- **Google Gemini (Generation Layer)**: Utilized for response generation. The model's large context window allows for extensive document retrieval without truncation, providing superior reasoning capabilities compared to smaller open-source alternatives.

## 2. RAG Pipeline Implementation

The information retrieval process follows a strictly defined pipeline to ensure relevance and accuracy.

### 2.1 Ingestion & Processing

Documents are processed through a multi-stage pipeline:

1.  **Extraction**: Text is extracted from source formats (PDF, DOCX, TXT) using specialized parsers.
2.  **Chunking**: Content is segmented into **500-word windows** with a **50-word overlap**. This granularity balances semantic completeness with retrieval precision, ensuring that the model receives sufficient context without dilution.

### 2.2 Vectorization & Retrieval

- **Local Embedding Model**: The system employs `sentence-transformers/all-MiniLM-L6-v2` for generating vector embeddings. Running this model locally avoids external API dependencies for the embedding step, significantly reducing per-request latency and operating costs.
- **Semantic Search**: Retrieval is performed via Cosine Similarity search within ChromaDB, returning the top-k most relevant text chunks.

### 2.3 Contextual Generation

The generation phase uses a strictly engineered system prompt that binds the LLM's response to the retrieved context. This constraint minimizes hallucination by forcing the model to cite information solely from the provided documents.

## 3. Deployment Constraints & Roadmap

### Current Limitations

- **Vertical Scalability**: The current usage of embedded ChromaDB restricts the system to a single instance.
- **Synchronous Ingestion**: Large file processing blocks the main thread in the current implementation.

### Future Improvements

1.  **Containerization**: Implement Docker support for consistent deployment environments.
2.  **Distributed Vector Store**: Migration to a client-server vector database architecture for horizontal scaling.
3.  **Asynchronous Processing**: Integration of a task queue (e.g., Celery) for background document ingestion.
4.  **Security Layer**: Implementation of API Key authentication or OAuth2 for endpoint protection.
