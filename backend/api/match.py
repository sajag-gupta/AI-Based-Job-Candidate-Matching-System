"""
Match API routes for candidate-job matching
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.database import get_db, User
from backend.api.auth import get_current_user
from backend.services import get_matching_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/match", tags=["Matching"])


@router.get("/candidate/{candidate_id}")
async def match_candidate_to_jobs(
    candidate_id: int,
    top_k: int = Query(default=10, ge=1, le=100),
    min_similarity: float = Query(default=0.5, ge=0.0, le=1.0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get top matching jobs for a candidate
    """
    try:
        matching_service = get_matching_service()
        matches = matching_service.match_candidate_to_jobs(
            db=db,
            candidate_id=candidate_id,
            top_k=top_k,
            min_similarity=min_similarity
        )
        
        if not matches:
            return {
                "candidate_id": candidate_id,
                "matches": [],
                "message": "No matching jobs found"
            }
        
        logger.info(f"Found {len(matches)} matches for candidate {candidate_id}")
        return {
            "candidate_id": candidate_id,
            "total_matches": len(matches),
            "matches": matches
        }
    
    except Exception as e:
        logger.error(f"Error matching candidate to jobs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error finding matches: {str(e)}"
        )


@router.get("/job/{job_id}")
async def match_job_to_candidates(
    job_id: int,
    top_k: int = Query(default=10, ge=1, le=100),
    min_similarity: float = Query(default=0.5, ge=0.0, le=1.0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get top matching candidates for a job
    """
    try:
        matching_service = get_matching_service()
        matches = matching_service.match_job_to_candidates(
            db=db,
            job_id=job_id,
            top_k=top_k,
            min_similarity=min_similarity
        )
        
        if not matches:
            return {
                "job_id": job_id,
                "matches": [],
                "message": "No matching candidates found"
            }
        
        logger.info(f"Found {len(matches)} matches for job {job_id}")
        return {
            "job_id": job_id,
            "total_matches": len(matches),
            "matches": matches
        }
    
    except Exception as e:
        logger.error(f"Error matching job to candidates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error finding matches: {str(e)}"
        )
