import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict
import os

from app.config import settings


class VectorStore:
    """
    Manages interactions with ChromaDB for vector storage and retrieval.
    """
    def __init__(self):
        """Initialize ChromaDB client and collection."""
        os.makedirs(settings.vector_db_path, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=settings.vector_db_path,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, chunks: List[str], doc_id: str, filename: str) -> int:
        """
        Add document chunks to the vector store.
        
        Args:
            chunks (List[str]): List of text chunks.
            doc_id (str): Unique identifier for the document.
            filename (str): Name of the original file.
            
        Returns:
            int: Number of chunks added.
        """
        chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        
        metadatas = [
            {
                "doc_id": doc_id,
                "filename": filename,
                "chunk_index": i,
            }
            for i in range(len(chunks))
        ]
        
        self.collection.add(
            documents=chunks,
            ids=chunk_ids,
            metadatas=metadatas
        )
        
        return len(chunks)
    
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search for relevant document chunks.
        
        Args:
            query (str): The search query.
            num_results (int, optional): Number of results to return. Defaults to 5.
            
        Returns:
            List[Dict]: List of search results with text, metadata, and distance.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=num_results,
            include=["documents", "metadatas", "distances"]
        )
        
        formatted_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "chunk_text": doc,
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i]
                })
        
        return formatted_results
    
    def list_documents(self) -> List[Dict]:
        """
        List all unique documents stored in the collection.
        
        Returns:
            List[Dict]: List of document metadata (doc_id, filename).
        """
        all_items = self.collection.get()
        
        unique_docs = {}
        if all_items["metadatas"]:
            for metadata in all_items["metadatas"]:
                doc_id = metadata.get("doc_id")
                if doc_id and doc_id not in unique_docs:
                    unique_docs[doc_id] = {
                        "doc_id": doc_id,
                        "filename": metadata.get("filename", "Unknown")
                    }
        
        return list(unique_docs.values())
