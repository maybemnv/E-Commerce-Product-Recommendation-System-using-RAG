import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict
import os

from app.config import settings


class VectorStore:
    def __init__(self):
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
