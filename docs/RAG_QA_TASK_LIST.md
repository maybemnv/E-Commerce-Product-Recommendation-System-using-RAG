# Detailed Task List - RAG Q&A System Implementation

## 📋 Project Setup (30 minutes)

### Task 1.1: Initialize Project
- [ ] Create project directory: `rag-qa-system`
- [ ] Initialize git repository: `git init`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment:
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`

### Task 1.2: Create Project Structure
```
rag-qa-system/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration
│   └── services/
│       ├── __init__.py
│       ├── document_processor.py
│       ├── vector_store.py
│       └── qa_service.py
├── uploads/                 # Temporary file storage
├── data/                    # Vector DB storage
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Task 1.3: Install Dependencies
Create `requirements.txt`:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0

# Document Processing
PyPDF2==3.0.1
python-docx==1.1.0

# Vector Database (choose one, Chroma recommended)
chromadb==0.4.18

# Embeddings & LLM
openai==1.3.7
# OR
# sentence-transformers==2.2.2

# Optional but recommended
langchain==0.0.340
langchain-community==0.0.1
```

- [ ] Run: `pip install -r requirements.txt`

### Task 1.4: Setup Environment Variables
Create `.env.example`:
```
# LLM API Keys (use one)
OPENAI_API_KEY=your_openai_api_key_here
# HUGGINGFACE_API_KEY=your_hf_key_here

# Vector DB Config
VECTOR_DB_PATH=./data/chroma_db

# Upload Settings
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=10
```

- [ ] Copy `.env.example` to `.env`
- [ ] Add your actual API keys to `.env`
- [ ] Add `.env` to `.gitignore`

---

## 🗂️ Document Processing Module (1.5 hours)

### Task 2.1: Create Configuration File
**File:** `app/config.py`

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    openai_api_key: str
    
    # Paths
    upload_dir: str = "./uploads"
    vector_db_path: str = "./data/chroma_db"
    
    # Processing Config
    max_file_size_mb: int = 10
    chunk_size: int = 500
    chunk_overlap: int = 50
    
    class Config:
        env_file = ".env"

settings = Settings()
```

- [ ] Implement configuration loader
- [ ] Test loading environment variables

### Task 2.2: Create Pydantic Models
**File:** `app/models.py`

```python
from pydantic import BaseModel
from typing import List, Optional

class DocumentUploadResponse(BaseModel):
    doc_id: str
    filename: str
    num_chunks: int
    message: str

class QuestionRequest(BaseModel):
    question: str
    max_chunks: Optional[int] = 5
    
class Source(BaseModel):
    chunk_text: str
    document: str
    relevance_score: float

class AnswerResponse(BaseModel):
    answer: str
    sources: List[Source]
    confidence: str
```

- [ ] Define all request/response models
- [ ] Add validation rules

### Task 2.3: Document Processor Service
**File:** `app/services/document_processor.py`

**Subtasks:**

- [ ] **2.3.1: File Upload Handler**
```python
import os
from fastapi import UploadFile
import uuid

async def save_uploaded_file(file: UploadFile) -> str:
    """Save uploaded file and return file path"""
    # Generate unique filename
    # Save to upload directory
    # Return file path
```

- [ ] **2.3.2: Text Extraction**
```python
def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using PyPDF2"""
    # Open PDF
    # Extract text from all pages
    # Return combined text

def extract_text_from_txt(file_path: str) -> str:
    """Read text file"""
    # Simply read the file
    
def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX using python-docx"""
    # Open DOCX
    # Extract paragraphs
    # Return combined text
```

- [ ] **2.3.3: Text Chunking**
```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks"""
    # Split text into sentences or words
    # Create chunks of specified size
    # Add overlap between chunks
    # Return list of chunks
```

**Testing Checklist:**
- [ ] Test PDF extraction with sample file
- [ ] Test TXT extraction
- [ ] Test DOCX extraction (optional)
- [ ] Verify chunking creates proper overlaps
- [ ] Test with edge cases (empty files, large files)

---

## 🗄️ Vector Store Module (1.5 hours)

### Task 3.1: Setup Vector Database
**File:** `app/services/vector_store.py`

**Subtasks:**

- [ ] **3.1.1: Initialize Chroma Client**
```python
import chromadb
from chromadb.config import Settings as ChromaSettings

class VectorStore:
    def __init__(self):
        # Initialize Chroma client
        # Create or load collection
```

- [ ] **3.1.2: Embedding Function**
```python
from chromadb.utils import embedding_functions

# Option 1: OpenAI Embeddings
def get_embedding_function():
    return embedding_functions.OpenAIEmbeddingFunction(
        api_key=settings.openai_api_key,
        model_name="text-embedding-ada-002"
    )

# Option 2: Sentence Transformers (free, local)
# from sentence_transformers import SentenceTransformer
```

- [ ] **3.1.3: Store Document Chunks**
```python
def add_documents(
    self,
    chunks: List[str],
    doc_id: str,
    filename: str
) -> int:
    """Add document chunks to vector store"""
    # Generate unique IDs for each chunk
    # Create metadata for each chunk
    # Add to collection
    # Return number of chunks added
```

- [ ] **3.1.4: Semantic Search**
```python
def search(
    self,
    query: str,
    num_results: int = 5
) -> List[dict]:
    """Search for relevant chunks"""
    # Query the collection
    # Return results with metadata and scores
```

**Testing Checklist:**
- [ ] Test database initialization
- [ ] Test adding sample chunks
- [ ] Test semantic search with queries
- [ ] Verify results are ranked by relevance
- [ ] Test with multiple documents

---

## 🤖 Question Answering Service (1.5 hours)

### Task 4.1: LLM Integration
**File:** `app/services/qa_service.py`

**Subtasks:**

- [ ] **4.1.1: Initialize OpenAI Client**
```python
from openai import OpenAI

class QAService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.client = OpenAI(api_key=settings.openai_api_key)
```

- [ ] **4.1.2: Prompt Engineering**
```python
def create_prompt(self, question: str, context: str) -> str:
    """Create RAG prompt with context"""
    prompt = f"""
    You are a helpful assistant answering questions based on provided context.
    
    Context:
    {context}
    
    Question: {question}
    
    Instructions:
    - Answer the question based ONLY on the context provided
    - If the answer is not in the context, say "I don't have enough information"
    - Be concise and accurate
    - Cite which part of the context you used
    
    Answer:
    """
    return prompt
```

- [ ] **4.1.3: Generate Answer**
```python
def generate_answer(
    self,
    question: str,
    max_chunks: int = 5
) -> dict:
    """Generate answer using RAG pipeline"""
    # 1. Retrieve relevant chunks from vector store
    # 2. Combine chunks into context
    # 3. Create prompt
    # 4. Call LLM
    # 5. Format response with sources
```

**Testing Checklist:**
- [ ] Test with sample question
- [ ] Verify context is properly retrieved
- [ ] Test LLM generates relevant answers
- [ ] Test "I don't know" responses
- [ ] Test with different chunk sizes

---

## 🚀 FastAPI Endpoints (1 hour)

### Task 5.1: Main Application Setup
**File:** `app/main.py`

- [ ] **5.1.1: Initialize FastAPI App**
```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RAG Q&A System",
    description="Document-based Q&A using RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- [ ] **5.1.2: Initialize Services**
```python
from app.services.vector_store import VectorStore
from app.services.qa_service import QAService

vector_store = VectorStore()
qa_service = QAService(vector_store)
```

### Task 5.2: Implement Endpoints

- [ ] **5.2.1: Health Check Endpoint**
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "RAG Q&A System is running"}
```

- [ ] **5.2.2: Document Upload Endpoint**
```python
@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document
    - Accepts PDF, TXT, DOCX files
    - Extracts text and creates embeddings
    - Stores in vector database
    """
    # 1. Validate file type and size
    # 2. Save uploaded file
    # 3. Extract text based on file type
    # 4. Chunk the text
    # 5. Add to vector store
    # 6. Return response with doc_id and stats
```

- [ ] **5.2.3: Question Answering Endpoint**
```python
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about uploaded documents
    - Retrieves relevant context
    - Generates answer using LLM
    - Returns answer with sources
    """
    # 1. Validate question
    # 2. Call QA service
    # 3. Format and return response
```

- [ ] **5.2.4: List Documents Endpoint (Optional)**
```python
@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    # Query vector store for document list
    # Return document metadata
```

**Testing Checklist:**
- [ ] Test each endpoint with curl/Postman
- [ ] Verify proper error handling
- [ ] Test file upload limits
- [ ] Test invalid requests return proper errors

---

## 🧪 Testing & Refinement (1 hour)

### Task 6.1: End-to-End Testing

- [ ] **6.1.1: Create Test Documents**
  - [ ] Create sample PDF about RAG
  - [ ] Create sample TXT with FAQs
  - [ ] Prepare test questions

- [ ] **6.1.2: Test Complete Flow**
  - [ ] Upload document via `/upload`
  - [ ] Ask question via `/ask`
  - [ ] Verify answer quality
  - [ ] Check source citations

- [ ] **6.1.3: Edge Case Testing**
  - [ ] Empty questions
  - [ ] Very long documents
  - [ ] Unsupported file types
  - [ ] Questions with no answer in docs

### Task 6.2: Error Handling

- [ ] Add try-catch blocks for:
  - [ ] File processing errors
  - [ ] Vector store errors
  - [ ] LLM API errors
  - [ ] Network errors

- [ ] Return proper HTTP status codes:
  - [ ] 200: Success
  - [ ] 400: Bad request
  - [ ] 404: Not found
  - [ ] 500: Server error

### Task 6.3: Logging

- [ ] Add logging throughout application
- [ ] Log important events:
  - [ ] Document uploads
  - [ ] Questions asked
  - [ ] Errors and exceptions

---

## 📝 Documentation (1 hour)

### Task 7.1: README.md

Create comprehensive README with:

- [ ] **7.1.1: Project Description**
  - What the project does
  - Key features
  - Technologies used

- [ ] **7.1.2: Setup Instructions**
  ```markdown
  ## Installation
  
  1. Clone the repository
  2. Create virtual environment
  3. Install dependencies
  4. Setup environment variables
  5. Run the application
  ```

- [ ] **7.1.3: API Documentation**
  - List all endpoints
  - Request/response examples
  - curl commands for testing

- [ ] **7.1.4: Usage Examples**
  ```markdown
  ## Example Usage
  
  ### Upload a Document
  curl -X POST "http://localhost:8000/upload" \
    -F "file=@document.pdf"
  
  ### Ask a Question
  curl -X POST "http://localhost:8000/ask" \
    -H "Content-Type: application/json" \
    -d '{"question": "What is RAG?"}'
  ```

- [ ] **7.1.5: Troubleshooting Section**

### Task 7.2: Design Decisions Document

Create `DESIGN_DECISIONS.md`:

- [ ] **7.2.1: Architecture Overview**
  - Why FastAPI?
  - Why Chroma DB?
  - Why specific embedding model?

- [ ] **7.2.2: RAG Implementation**
  - Chunking strategy explanation
  - Embedding choice rationale
  - Prompt engineering approach

- [ ] **7.2.3: Trade-offs Made**
  - What features were prioritized
  - What was left out and why
  - Performance vs accuracy decisions

### Task 7.3: Code Comments

- [ ] Review all code files
- [ ] Add docstrings to all functions
- [ ] Add inline comments for complex logic
- [ ] Add type hints everywhere

---

## 🚢 Final Submission Preparation (30 minutes)

### Task 8.1: Code Cleanup

- [ ] Remove debug print statements
- [ ] Remove unused imports
- [ ] Format code consistently (use Black)
- [ ] Check for hardcoded values

### Task 8.2: Pre-Submission Checklist

- [ ] All endpoints working
- [ ] README is complete and accurate
- [ ] requirements.txt has exact versions
- [ ] .env.example is included (no real keys)
- [ ] .gitignore includes .env, uploads/, data/
- [ ] Code is well-commented
- [ ] Design decisions documented

### Task 8.3: Repository/Package Preparation

**If GitHub:**
- [ ] Create GitHub repository
- [ ] Push all code
- [ ] Verify repository is public
- [ ] Test cloning and setup from scratch

**If Zipped:**
- [ ] Create clean project folder
- [ ] Remove __pycache__, .pyc files
- [ ] Remove uploads/ and data/ content
- [ ] Zip the folder
- [ ] Test extracting and running

### Task 8.4: Email Submission

Prepare email to hrteam@vtuae.com:

```
Subject: Backend Developer Assignment Submission - [Your Name]

Dear Hiring Team,

Please find my submission for the Backend Developer position assignment.

Project: Document-Based Q&A System using RAG
GitHub Link: [your-github-link] OR Attached: rag-qa-system.zip

Key Features Implemented:
- Document upload (PDF, TXT support)
- Vector database integration with Chroma
- RAG pipeline with OpenAI/[your choice]
- REST API with FastAPI
- Comprehensive documentation

Setup time: ~10 minutes
Tech Stack: FastAPI, ChromaDB, OpenAI, LangChain

Please let me know if you need any clarification.

Best regards,
[Your Name]
[Your Contact]
```

---

## ⏱️ Time Allocation Summary

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Setup | 1.1 - 1.4 | 30 min |
| Document Processing | 2.1 - 2.3 | 1.5 hours |
| Vector Store | 3.1 | 1.5 hours |
| QA Service | 4.1 | 1.5 hours |
| API Endpoints | 5.1 - 5.2 | 1 hour |
| Testing | 6.1 - 6.3 | 1 hour |
| Documentation | 7.1 - 7.3 | 1 hour |
| Submission Prep | 8.1 - 8.4 | 30 min |
| **Total** | | **~6-8 hours** |

---

## 💡 Pro Tips

1. **Start Simple:** Get a basic working version first, then add features
2. **Test as You Go:** Don't wait until the end to test
3. **Document Early:** Write README sections as you complete features
4. **Use Free Tools:** Start with Chroma + OpenAI/HuggingFace to avoid costs
5. **Commit Often:** If using Git, commit after each major task
6. **Ask for Help:** If stuck for >30 min, search Stack Overflow or docs
7. **Time Management:** Set a timer for each phase to stay on track

---

## 🎯 Minimum Viable Product (MVP)

If short on time, prioritize these:

**Must Have:**
- ✅ PDF upload and text extraction
- ✅ Chroma vector database setup
- ✅ Basic embedding storage
- ✅ `/upload` and `/ask` endpoints working
- ✅ Simple README with setup steps

**Can Skip if Needed:**
- ⏭️ DOCX support (stick to PDF + TXT)
- ⏭️ Document listing/deletion
- ⏭️ Advanced error handling
- ⏭️ Fancy logging
- ⏭️ Streaming responses

Good luck! You got this! 🚀
