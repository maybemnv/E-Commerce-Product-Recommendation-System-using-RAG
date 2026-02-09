from typing import List, Dict
import google.generativeai as genai

from app.config import settings
from app.services.vector_store import VectorStore


class QAService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-3-flash-preview')
        else:
            self.model = None
    
    def create_prompt(self, question: str, context: str) -> str:
        return f"""You are a helpful assistant answering questions based on provided context.

Context:
{context}

Question: {question}

Instructions:
- Answer the question based ONLY on the context provided
- If the answer is not in the context, say "I don't have enough information to answer this question"
- Be concise and accurate
- Cite which part of the context you used if relevant

Answer:"""
    
    def generate_answer(self, question: str, max_chunks: int = 5) -> Dict:
        search_results = self.vector_store.search(query=question, num_results=max_chunks)
        
        if not search_results:
            return {
                "answer": "No relevant information found in the uploaded documents.",
                "sources": [],
                "confidence": "none"
            }
        
        context = "\n\n".join([
            f"[Source {i+1}]: {result['chunk_text']}"
            for i, result in enumerate(search_results)
        ])
        
        if not self.model:
            return {
                "answer": "Gemini API key not configured. Please set GEMINI_API_KEY in .env file.",
                "sources": self._format_sources(search_results),
                "confidence": "none"
            }
        
        try:
            prompt = self.create_prompt(question, context)
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.3,
                    'max_output_tokens': 500,
                }
            )
            
            answer = response.text.strip()
            confidence = self._calculate_confidence(search_results)
            
            return {
                "answer": answer,
                "sources": self._format_sources(search_results),
                "confidence": confidence
            }
        
        except Exception as e:
            return {
                "answer": f"Error generating answer: {str(e)}",
                "sources": self._format_sources(search_results),
                "confidence": "error"
            }
    
    def _format_sources(self, search_results: List[Dict]) -> List[Dict]:
        sources = []
        for result in search_results:
            sources.append({
                "chunk_text": result["chunk_text"][:200] + "...",
                "document": result["metadata"].get("filename", "Unknown"),
                "relevance_score": 1.0 - result["distance"]
            })
        return sources
    
    def _calculate_confidence(self, search_results: List[Dict]) -> str:
        if not search_results:
            return "none"
        
        avg_distance = sum(r["distance"] for r in search_results) / len(search_results)
        
        if avg_distance < 0.3:
            return "high"
        elif avg_distance < 0.6:
            return "medium"
        else:
            return "low"
