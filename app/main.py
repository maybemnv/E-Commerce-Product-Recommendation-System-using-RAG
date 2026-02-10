import os
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import DocumentUploadResponse, QuestionRequest, AnswerResponse
from app.services.document_processor import save_uploaded_file, extract_text, chunk_text
from app.services.vector_store import VectorStore
from app.services.qa_service import QAService


app = FastAPI(
    title="RAG Q&A System",
    description="Document-based Question & Answering using RAG",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = VectorStore()
qa_service = QAService(vector_store)


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify system status.
    
    Returns:
        dict: Status message indicating the API is running.
    """
    return {
        "status": "healthy",
        "message": "RAG Q&A System is running"
    }


@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document (PDF, TXT, DOCX).
    
    Validates file type and size, extracts text, chunks it, and stores 
    embeddings in the vector database.
    
    Args:
        file (UploadFile): The uploaded file object.
        
    Returns:
        DocumentUploadResponse: Metadata about the processed document including doc_id.
        
    Raises:
        HTTPException: If file type is unsupported, file is too large, 
                       or processing fails.
    """
    allowed_extensions = {".pdf", ".txt", ".docx"}
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_extension} not supported. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    file.file.seek(0, 2)
    file_size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)
    
    if file_size_mb > settings.max_file_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File size ({file_size_mb:.2f}MB) exceeds maximum allowed size ({settings.max_file_size_mb}MB)"
        )
    
    try:
        file_path = await save_uploaded_file(file)
        
        text = extract_text(file_path)
        
        if not text.strip():
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="No text content found in document")
        
        chunks = chunk_text(text)
        
        doc_id = str(uuid.uuid4())
        
        num_chunks = vector_store.add_documents(
            chunks=chunks,
            doc_id=doc_id,
            filename=file.filename
        )
        
        return DocumentUploadResponse(
            doc_id=doc_id,
            filename=file.filename,
            num_chunks=num_chunks,
            message="Document uploaded and processed successfully"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question based on uploaded documents.
    
    Retrieves relevant context from the vector store and uses the LLM
    to generate an answer with source citations.
    
    Args:
        request (QuestionRequest): The question and optional configuration.
        
    Returns:
        AnswerResponse: The generated answer, sources, and confidence score.
        
    Raises:
        HTTPException: If answer generation fails.
    """
    try:
        result = qa_service.generate_answer(
            question=request.question,
            max_chunks=request.max_chunks
        )
        
        return AnswerResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")


@app.get("/documents")
async def list_documents():
    """
    List all uploaded documents available in the vector store.
    
    Returns:
        dict: Total count and list of document metadata.
        
    Raises:
        HTTPException: If listing documents fails.
    """
    try:
        documents = vector_store.list_documents()
        return {
            "total": len(documents),
            "documents": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")
