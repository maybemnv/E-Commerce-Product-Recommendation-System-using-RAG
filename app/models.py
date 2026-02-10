from pydantic import BaseModel, Field
from typing import List, Optional


class DocumentUploadResponse(BaseModel):
    """Response model for document upload operations."""
    doc_id: str
    filename: str
    num_chunks: int
    message: str


class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    question: str = Field(..., min_length=1)
    max_chunks: Optional[int] = Field(default=5, ge=1, le=20)


class Source(BaseModel):
    """Model representing a source chunk used for an answer."""
    chunk_text: str
    document: str
    relevance_score: float


class AnswerResponse(BaseModel):
    """Response model for generated answers."""
    answer: str
    sources: List[Source]
    confidence: str
