"""
Search API routes for filtering candidates and jobs
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
import logging

from backend.database import get_db, Candidate, Job, User
from backend.api.schemas import CandidateResponse, JobResponse
from backend.api.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/candidates", response_model=List[CandidateResponse])
async def search_candidates(
    skills: Optional[str] = Query(None, description="Comma-separated skills"),
    min_experience: Optional[float] = Query(None, ge=0),
    max_experience: Optional[float] = Query(None, ge=0),
    name: Optional[str] = Query(None),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search and filter candidates
    """
    try:
        query = db.query(Candidate)
        
        # Filter by name
        if name:
            query = query.filter(Candidate.name.ilike(f"%{name}%"))
        
        # Filter by experience
        if min_experience is not None:
            query = query.filter(Candidate.experience_years >= min_experience)
        if max_experience is not None:
            query = query.filter(Candidate.experience_years <= max_experience)
        
        # Filter by skills
        if skills:
            skill_list = [s.strip().lower() for s in skills.split(',')]
            # This is a simple approach; for production, use PostgreSQL array operations
            for skill in skill_list:
                query = query.filter(Candidate.raw_text.ilike(f"%{skill}%"))
        
        candidates = query.limit(limit).all()
        logger.info(f"Found {len(candidates)} candidates matching search criteria")
        
        return candidates
    
    except Exception as e:
        logger.error(f"Error searching candidates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching candidates: {str(e)}"
        )


@router.get("/jobs", response_model=List[JobResponse])
async def search_jobs(
    title: Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    skills: Optional[str] = Query(None, description="Comma-separated skills"),
    min_experience: Optional[float] = Query(None, ge=0),
    max_experience: Optional[float] = Query(None, ge=0),
    location: Optional[str] = Query(None),
    job_type: Optional[str] = Query(None),
    seniority_level: Optional[str] = Query(None),
    domain: Optional[str] = Query(None),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search and filter jobs
    """
    try:
        query = db.query(Job)
        
        # Filter by title
        if title:
            query = query.filter(Job.title.ilike(f"%{title}%"))
        
        # Filter by company
        if company:
            query = query.filter(Job.company.ilike(f"%{company}%"))
        
        # Filter by location
        if location:
            query = query.filter(Job.location.ilike(f"%{location}%"))
        
        # Filter by job type
        if job_type:
            query = query.filter(Job.job_type == job_type)
        
        # Filter by seniority level
        if seniority_level:
            query = query.filter(Job.seniority_level == seniority_level)
        
        # Filter by domain
        if domain:
            query = query.filter(Job.domain == domain)
        
        # Filter by experience
        if min_experience is not None:
            query = query.filter(Job.experience_required >= min_experience)
        if max_experience is not None:
            query = query.filter(Job.experience_required <= max_experience)
        
        # Filter by skills
        if skills:
            skill_list = [s.strip().lower() for s in skills.split(',')]
            for skill in skill_list:
                query = query.filter(Job.description.ilike(f"%{skill}%"))
        
        jobs = query.limit(limit).all()
        logger.info(f"Found {len(jobs)} jobs matching search criteria")
        
        return jobs
    
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching jobs: {str(e)}"
        )
