# Design Decisions

## Architecture

- **FastAPI**: Chosen for performance (async support) and automatic documentation.
- **ChromaDB**: Selected as the vector store for its ease of local setup and zero-configuration persistence.
- **Google Gemini**: Utilized for generation due to performance-to-cost ratio and efficient context handling.

## Implementation

- **Chunking**: Documents are split into 500-word chunks with 50-word overlap to preserve context boundaries.
- **Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` locally to avoid external API latency and costs for vectorization.
- **Prompting**: Strict system prompts enforce answers solely based on retrieved context to minimize hallucinations.

## Limitations

- **Local Persistence**: Vector data is stored on disk (SQLite/Chroma), suitable for single-instance deployments.
- **File Support**: Currently optimized for text-based PDF, DOCX, and TXT files.
