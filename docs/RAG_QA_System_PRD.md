# Product Requirements Document (PRD)
## Document-Based Q&A System using RAG

**Assignment for:** Vikashan Technologies - Backend Developer Position  
**Estimated Time:** 4-6 hours  
**Due:** Within 7 days of receipt

---

## 1. Project Overview

Build an intelligent Question & Answer system that allows users to upload documents, processes them into a searchable knowledge base, and provides accurate answers to user queries using Retrieval Augmented Generation (RAG).

### Core Value Proposition
- Users can upload documents (PDF, TXT, DOCX) to create a knowledge base
- System semantically searches through documents to find relevant information
- LLM generates accurate, contextual answers based on retrieved document chunks

---

## 2. Technical Stack Requirements

### Backend Framework
- **FastAPI** (Python)
- RESTful API architecture

### Vector Database (Choose one)
- Chroma (recommended for simplicity)
- Pinecone
- Milvus
- Weaviate

### LLM Integration (Choose one)
- OpenAI API (GPT-3.5/4)
- HuggingFace models
- Ollama (local models)
- Google Gemini API

### Embeddings
- OpenAI embeddings
- HuggingFace sentence-transformers
- Other open-source embedding models

### Additional Libraries
- LangChain (optional but recommended)
- PyPDF2 / pdfplumber (for PDF processing)
- python-docx (for DOCX processing)
- python-dotenv (environment management)

---

## 3. Core Features & Requirements

### 3.1 Document Upload & Processing
**Endpoint:** `POST /upload`

**Functionality:**
- Accept document uploads (PDF, TXT, DOCX)
- Extract text content from documents
- Split text into chunks (500-1000 tokens recommended)
- Generate vector embeddings for each chunk
- Store chunks and embeddings in vector database

**Success Criteria:**
- Handles multiple document formats
- Efficient text chunking with overlap
- Proper error handling for invalid files

---

### 3.2 Semantic Search
**Endpoint:** `POST /search` (optional standalone endpoint)

**Functionality:**
- Accept search query as input
- Convert query to vector embedding
- Perform similarity search in vector database
- Return top-k most relevant document chunks (k=3-5)

**Success Criteria:**
- Returns contextually relevant chunks
- Fast retrieval (< 2 seconds)
- Configurable similarity threshold

---

### 3.3 Question Answering
**Endpoint:** `POST /ask`

**Functionality:**
- Accept user question as input
- Retrieve relevant document chunks using semantic search
- Construct prompt with context + question
- Generate answer using LLM
- Return answer with source references

**Success Criteria:**
- Accurate, contextual answers
- Citations/references to source documents
- Handles "I don't know" when information isn't in documents
- Response time < 5 seconds

---

### 3.4 Additional Endpoints (Optional but Recommended)

**Health Check**
- `GET /health` - API status check

**List Documents**
- `GET /documents` - List uploaded documents

**Delete Document**
- `DELETE /documents/{doc_id}` - Remove document from knowledge base

---

## 4. System Architecture

```
User Request
    ↓
FastAPI Server
    ↓
Document Processing → Text Extraction → Chunking → Embeddings
    ↓
Vector Database (Chroma/Pinecone)
    ↓
Query → Embedding → Similarity Search → Retrieve Context
    ↓
LLM (OpenAI/HuggingFace) → Generate Answer
    ↓
Response to User
```

---

## 5. Data Models

### Document Metadata
```python
{
    "doc_id": "uuid",
    "filename": "document.pdf",
    "upload_date": "2024-02-09",
    "num_chunks": 25,
    "file_size": "2.5MB"
}
```

### Query Request
```python
{
    "question": "What is RAG?",
    "max_chunks": 5,  # optional
    "temperature": 0.7  # optional
}
```

### Query Response
```python
{
    "answer": "RAG stands for...",
    "sources": [
        {
            "chunk_text": "...",
            "document": "rag_paper.pdf",
            "relevance_score": 0.89
        }
    ],
    "confidence": "high"
}
```

---

## 6. Non-Functional Requirements

### Code Quality
- Clean, readable code with meaningful variable names
- Comprehensive comments explaining logic
- Type hints for function parameters
- Error handling and logging

### Documentation
- **README.md** with:
  - Project description
  - Setup instructions (step-by-step)
  - API endpoint documentation
  - Example requests/responses
  - Environment variables needed
  - Troubleshooting guide
- **requirements.txt** with all dependencies
- Inline code comments
- Design decisions explanation

### Performance
- Document processing: < 30 seconds for 10-page PDF
- Query response: < 5 seconds
- Support for documents up to 100 pages

### Security
- Input validation
- File type verification
- Size limits on uploads
- API key protection (environment variables)

---

## 7. Deliverables Checklist

- [ ] Source code with clean structure
- [ ] README.md with complete setup guide
- [ ] requirements.txt with exact versions
- [ ] .env.example file (don't include actual API keys)
- [ ] API documentation (endpoints, request/response format)
- [ ] Design decisions document explaining:
  - Why you chose specific libraries
  - How you implemented chunking strategy
  - Your RAG pipeline design
  - Any trade-offs you made
- [ ] GitHub repository OR zipped folder

---

## 8. Evaluation Criteria

The assignment will likely be evaluated on:

1. **RAG Implementation (40%)**
   - Correct implementation of retrieval pipeline
   - Quality of embeddings and chunking strategy
   - LLM integration and prompt engineering

2. **Code Quality (25%)**
   - Clean, readable, well-structured code
   - Proper error handling
   - Good practices (separation of concerns, DRY)

3. **API Design (15%)**
   - RESTful design principles
   - Clear endpoint structure
   - Proper HTTP methods and status codes

4. **Documentation (15%)**
   - Clear README with setup instructions
   - Code comments
   - Design decisions explanation

5. **Completeness (5%)**
   - All required features implemented
   - Working end-to-end system

---

## 9. Success Metrics

**Must Have:**
- ✅ Document upload works for at least PDF and TXT
- ✅ Vector database successfully stores embeddings
- ✅ Q&A endpoint returns relevant answers
- ✅ Minimum 2-3 working API endpoints
- ✅ README with clear setup instructions

**Nice to Have:**
- ⭐ Support for multiple document formats
- ⭐ Streaming responses
- ⭐ Document management (list, delete)
- ⭐ Conversation history/context
- ⭐ Configurable parameters (chunk size, model, etc.)

---

## 10. Timeline Suggestion

- **Hour 1-2:** Setup + Document Processing
- **Hour 2-3:** Vector Database Integration + Embeddings
- **Hour 3-4:** RAG Pipeline + LLM Integration
- **Hour 4-5:** API Endpoints + Testing
- **Hour 5-6:** Documentation + Cleanup

---

## 11. Recommended Approach

1. Start simple: Get basic PDF upload + text extraction working
2. Implement vector storage with a simple database (Chroma is easiest)
3. Build the RAG pipeline step by step
4. Test with sample documents before polishing
5. Document as you go (don't leave it for the end)
6. Add nice-to-have features only if time permits

**Remember:** A working, well-documented simple system is better than a complex, broken one!
