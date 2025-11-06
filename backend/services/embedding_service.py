"""
Embedding Service using Sentence-BERT for semantic similarity
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import logging
from functools import lru_cache

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EmbeddingService:
    """Service for generating and managing embeddings"""
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Sentence-BERT model"""
        try:
            logger.info(f"Loading embedding model: {settings.MODEL_NAME}")
            self.model = SentenceTransformer(settings.MODEL_NAME)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for a single text
        """
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for embedding")
                return [0.0] * settings.EMBEDDING_DIM
            
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch processing)
        """
        try:
            if not texts:
                return []
            
            embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise
    
    @staticmethod
    def cosine_similarity(vec1: Union[List[float], np.ndarray], 
                         vec2: Union[List[float], np.ndarray]) -> float:
        """
        Calculate cosine similarity between two vectors
        """
        try:
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0
    
    @staticmethod
    def calculate_similarity_matrix(embeddings1: List[List[float]], 
                                   embeddings2: List[List[float]]) -> np.ndarray:
        """
        Calculate similarity matrix between two sets of embeddings
        """
        try:
            mat1 = np.array(embeddings1)
            mat2 = np.array(embeddings2)
            
            # Normalize vectors
            mat1_norm = mat1 / np.linalg.norm(mat1, axis=1, keepdims=True)
            mat2_norm = mat2 / np.linalg.norm(mat2, axis=1, keepdims=True)
            
            # Compute similarity matrix
            similarity_matrix = np.dot(mat1_norm, mat2_norm.T)
            return similarity_matrix
        except Exception as e:
            logger.error(f"Error calculating similarity matrix: {e}")
            raise


# Singleton instance
@lru_cache()
def get_embedding_service() -> EmbeddingService:
    """Get singleton embedding service instance"""
    return EmbeddingService()
