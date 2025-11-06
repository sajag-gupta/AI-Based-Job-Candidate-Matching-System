"""
Matching Service for candidate-job matching using embeddings
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
import logging
from functools import lru_cache

from backend.database.models import Candidate, Job, Embedding, MatchResult
from backend.services.embedding_service import get_embedding_service
from backend.services.nlp_service import NLPService

logger = logging.getLogger(__name__)


class MatchingService:
    """Service for matching candidates with jobs"""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
        self.nlp_service = NLPService()
        self._match_cache = {}
    
    def match_candidate_to_jobs(self, 
                                db: Session,
                                candidate_id: int,
                                top_k: int = 10,
                                min_similarity: float = 0.5) -> List[Dict]:
        """
        Find top matching jobs for a candidate
        """
        try:
            # Get candidate and embedding
            candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
            if not candidate:
                logger.error(f"Candidate {candidate_id} not found")
                return []
            
            candidate_embedding = db.query(Embedding).filter(
                Embedding.candidate_id == candidate_id
            ).first()
            
            if not candidate_embedding:
                logger.error(f"No embedding found for candidate {candidate_id}")
                return []
            
            # Get all job embeddings
            job_embeddings = db.query(Embedding).filter(
                Embedding.job_id.isnot(None)
            ).all()
            
            matches = []
            for job_emb in job_embeddings:
                job = db.query(Job).filter(Job.id == job_emb.job_id).first()
                if not job:
                    continue
                
                # Calculate similarity
                similarity = self.embedding_service.cosine_similarity(
                    candidate_embedding.embedding_vector,
                    job_emb.embedding_vector
                )
                
                if similarity >= min_similarity:
                    # Calculate skill overlap
                    skill_overlap = self.nlp_service.calculate_skill_overlap(
                        candidate.skills or [],
                        job.required_skills or []
                    )
                    
                    matches.append({
                        'job_id': job.id,
                        'job_title': job.title,
                        'company': job.company,
                        'similarity_score': round(similarity * 100, 2),
                        'skill_overlap': skill_overlap,
                        'location': job.location,
                        'job_type': job.job_type
                    })
            
            # Sort by similarity score
            matches.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            # Store top matches in database
            self._store_match_results(db, candidate_id, matches[:top_k])
            
            return matches[:top_k]
        
        except Exception as e:
            logger.error(f"Error matching candidate to jobs: {e}")
            raise
    
    def match_job_to_candidates(self,
                                db: Session,
                                job_id: int,
                                top_k: int = 10,
                                min_similarity: float = 0.5) -> List[Dict]:
        """
        Find top matching candidates for a job
        """
        try:
            # Get job and embedding
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                logger.error(f"Job {job_id} not found")
                return []
            
            job_embedding = db.query(Embedding).filter(
                Embedding.job_id == job_id
            ).first()
            
            if not job_embedding:
                logger.error(f"No embedding found for job {job_id}")
                return []
            
            # Get all candidate embeddings
            candidate_embeddings = db.query(Embedding).filter(
                Embedding.candidate_id.isnot(None)
            ).all()
            
            matches = []
            for cand_emb in candidate_embeddings:
                candidate = db.query(Candidate).filter(
                    Candidate.id == cand_emb.candidate_id
                ).first()
                if not candidate:
                    continue
                
                # Calculate similarity
                similarity = self.embedding_service.cosine_similarity(
                    job_embedding.embedding_vector,
                    cand_emb.embedding_vector
                )
                
                if similarity >= min_similarity:
                    # Calculate skill overlap
                    skill_overlap = self.nlp_service.calculate_skill_overlap(
                        candidate.skills or [],
                        job.required_skills or []
                    )
                    
                    matches.append({
                        'candidate_id': candidate.id,
                        'candidate_name': candidate.name,
                        'email': candidate.email,
                        'similarity_score': round(similarity * 100, 2),
                        'skill_overlap': skill_overlap,
                        'experience_years': candidate.experience_years
                    })
            
            # Sort by similarity score
            matches.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            # Store top matches in database
            self._store_match_results(db, None, matches[:top_k], job_id=job_id)
            
            return matches[:top_k]
        
        except Exception as e:
            logger.error(f"Error matching job to candidates: {e}")
            raise
    
    def _store_match_results(self, 
                            db: Session,
                            candidate_id: Optional[int] = None,
                            matches: List[Dict] = None,
                            job_id: Optional[int] = None):
        """
        Store match results in database
        """
        try:
            if candidate_id and matches:
                for match in matches:
                    existing = db.query(MatchResult).filter(
                        MatchResult.candidate_id == candidate_id,
                        MatchResult.job_id == match['job_id']
                    ).first()
                    
                    if existing:
                        existing.similarity_score = match['similarity_score'] / 100
                        existing.skill_overlap = match['skill_overlap']
                    else:
                        new_match = MatchResult(
                            candidate_id=candidate_id,
                            job_id=match['job_id'],
                            similarity_score=match['similarity_score'] / 100,
                            skill_overlap=match['skill_overlap']
                        )
                        db.add(new_match)
            
            elif job_id and matches:
                for match in matches:
                    existing = db.query(MatchResult).filter(
                        MatchResult.candidate_id == match['candidate_id'],
                        MatchResult.job_id == job_id
                    ).first()
                    
                    if existing:
                        existing.similarity_score = match['similarity_score'] / 100
                        existing.skill_overlap = match['skill_overlap']
                    else:
                        new_match = MatchResult(
                            candidate_id=match['candidate_id'],
                            job_id=job_id,
                            similarity_score=match['similarity_score'] / 100,
                            skill_overlap=match['skill_overlap']
                        )
                        db.add(new_match)
            
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Error storing match results: {e}")


# Singleton instance
@lru_cache()
def get_matching_service() -> MatchingService:
    """Get singleton matching service instance"""
    return MatchingService()
