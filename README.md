# RAG Q&A System

A document-based Question & Answering system using Retrieval-Augmented Generation (RAG) with Google Gemini AI.

## Features

- Upload and process documents (PDF, TXT, DOCX)
- Semantic search with ChromaDB vector database
- Context-aware answers using Google Gemini Pro
- RESTful API with FastAPI
- Source attribution and confidence scoring

## Tech Stack

- **Framework**: FastAPI
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (local, free)
- **LLM**: Google Gemini Pro
- **Document Processing**: PyPDF2, python-docx

## Setup

### Prerequisites

- Python 3.8+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

```bash
git clone <repository-url>
cd "E-Commerce Product Recommendation System using RAG"

uv sync
```

### Configuration

1. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. Add your Gemini API key to `.env`:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

## Running the Application

```bash
uv run python main.py
```

Or using uvicorn directly:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

### Upload Document

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@path/to/document.pdf"
```

**Response:**

```json
{
  "doc_id": "uuid-here",
  "filename": "document.pdf",
  "num_chunks": 45,
  "message": "Document uploaded and processed successfully"
}
```

### Ask Question

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is RAG?",
    "max_chunks": 5
  }'
```

**Response:**

```json
{
  "answer": "RAG (Retrieval-Augmented Generation) is...",
  "sources": [
    {
      "chunk_text": "Relevant text excerpt...",
      "document": "document.pdf",
      "relevance_score": 0.95
    }
  ],
  "confidence": "high"
}
```

### List Documents

```bash
curl http://localhost:8000/documents
```

## Usage Example

1. Start the server
2. Upload a document:

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@test_rag_document.txt"
```

3. Ask questions:

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

## Configuration Options

Edit `.env` to customize:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `VECTOR_DB_PATH`: ChromaDB storage path (default: ./data/chroma_db)
- `UPLOAD_DIR`: Uploaded files directory (default: ./uploads)
- `MAX_FILE_SIZE_MB`: Maximum file size in MB (default: 10)
- `CHUNK_SIZE`: Text chunk size in words (default: 500)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)

## Architecture

1. **Document Upload**: Files are uploaded, text extracted, and split into chunks
2. **Vector Storage**: Chunks are embedded and stored in ChromaDB
3. **Query Processing**: Questions are embedded and matched against stored chunks
4. **Answer Generation**: Relevant chunks are sent to Gemini Pro as context
5. **Response**: Answer with source attribution and confidence score

## Supported File Types

- PDF (.pdf)
- Text (.txt)
- Word Documents (.docx)

## Development

### Project Structure

```
app/
├── __init__.py
├── main.py                    # FastAPI application
├── config.py                  # Configuration management
├── models.py                  # Pydantic models
└── services/
    ├── __init__.py
    ├── document_processor.py  # File upload & text extraction
    ├── vector_store.py        # ChromaDB integration
    └── qa_service.py          # RAG pipeline & Gemini integration
```

## License

MIT
