from pydantic import BaseModel, Field
from typing import List, Optional


class DocumentUploadResponse(BaseModel):
    doc_id: str
    filename: str
    num_chunks: int
    message: str


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)
    max_chunks: Optional[int] = Field(default=5, ge=1, le=20)


class Source(BaseModel):
    chunk_text: str
    document: str
    relevance_score: float


class AnswerResponse(BaseModel):
    answer: str
    sources: List[Source]
    confidence: str
