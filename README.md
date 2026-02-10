# RAG Q&A System

A document-based Question & Answering system using Retrieval-Augmented Generation (RAG).

## Features

- **Document Ingestion**: Support for PDF, TXT, and DOCX formats.
- **RAG Pipeline**: Semantic search using ChromaDB and answer generation via Google Gemini.
- **REST API**: Built with FastAPI.

## Tech Stack

- **Framework**: FastAPI
- **Vector Store**: ChromaDB
- **LLM**: Google Gemini (gemini-2.5-flash-lite)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)

For a detailed breakdown of architectural choices, see [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).

## Setup

1.  **Clone & Install**

    ```bash
    git clone <repo-url>
    cd rag-qa-system
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Configuration**
    Copy `.env.example` to `.env` and set your API key:

    ```ini
    GEMINI_API_KEY=your_key_here
    ```

3.  **Run**
    ```bash
    uvicorn app.main:app --reload
    ```

## API Usage

- **POST /upload**: Upload a document file.
- **POST /ask**: Ask a question about the uploaded content.
- **GET /documents**: List available documents.

Documentation available at `http://localhost:8000/docs`.
