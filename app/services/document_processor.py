import os
import uuid
from pathlib import Path
from typing import List
from fastapi import UploadFile
import PyPDF2
from docx import Document

from app.config import settings


async def save_uploaded_file(file: UploadFile) -> str:
    """
    Save an uploaded file to disk with a unique filename.
    
    Args:
        file (UploadFile): The uploaded file object.
        
    Returns:
        str: The absolute path to the saved file.
    """
    os.makedirs(settings.upload_dir, exist_ok=True)
    
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.upload_dir, unique_filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return file_path


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text content from a PDF file."""
    text = []
    with open(file_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def extract_text_from_txt(file_path: str) -> str:
    """Extract text content from a plain text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text_from_docx(file_path: str) -> str:
    """Extract text content from a DOCX file."""
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


def extract_text(file_path: str) -> str:
    """
    Extract text from a file based on its extension.
    
    Supported extensions: .pdf, .txt, .docx
    
    Args:
        file_path (str): Path to the file.
        
    Returns:
        str: Extracted text content.
        
    Raises:
        ValueError: If file type is not supported.
    """
    extension = Path(file_path).suffix.lower()
    
    extractors = {
        ".pdf": extract_text_from_pdf,
        ".txt": extract_text_from_txt,
        ".docx": extract_text_from_docx,
    }
    
    extractor = extractors.get(extension)
    if not extractor:
        raise ValueError(f"Unsupported file type: {extension}")
    
    return extractor(file_path)


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text (str): The input text to chunk.
        chunk_size (int, optional): Size of each chunk in words. Defaults to setting.
        overlap (int, optional): Number of overlapping words. Defaults to setting.
        
    Returns:
        List[str]: List of text chunks.
    """
    if chunk_size is None:
        chunk_size = settings.chunk_size
    if overlap is None:
        overlap = settings.chunk_overlap
    
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        
        if i + chunk_size >= len(words):
            break
    
    return chunks
