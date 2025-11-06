"""
Upload API routes for resumes and job descriptions
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import logging
import os
from pathlib import Path
import shutil

from backend.database import get_db, Candidate, Job, Embedding, User
from backend.api.schemas import CandidateResponse, JobResponse, JobCreate
from backend.api.auth import get_current_user
from backend.services import ResumeParser, JobParser, get_embedding_service
from backend.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/upload", tags=["Upload"])
settings = get_settings()

# Create uploads directory
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/resume", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload and process a resume file (PDF/DOCX)
    """
    try:
        # Validate file type
        if not file.filename.endswith(('.pdf', '.docx', '.doc')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF and DOCX files are supported"
            )
        
        # Save file
        file_path = UPLOAD_DIR / f"{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Resume file saved: {file_path}")
        
        # Parse resume
        parser = ResumeParser()
        parsed_data = parser.parse_file(str(file_path))
        
        # Check if candidate already exists
        existing_candidate = None
        if parsed_data.get('email'):
            existing_candidate = db.query(Candidate).filter(
                Candidate.email == parsed_data['email']
            ).first()
        
        if existing_candidate:
            # Update existing candidate
            for key, value in parsed_data.items():
                if key != 'raw_text':  # Don't overwrite raw_text
                    setattr(existing_candidate, key, value)
            existing_candidate.file_path = str(file_path)
            db.commit()
            db.refresh(existing_candidate)
            candidate = existing_candidate
            logger.info(f"Updated existing candidate: {candidate.id}")
        else:
            # Create new candidate
            candidate = Candidate(
                name=parsed_data['name'],
                email=parsed_data.get('email'),
                phone=parsed_data.get('phone'),
                skills=parsed_data['skills'],
                experience_years=parsed_data['experience_years'],
                education=parsed_data['education'],
                raw_text=parsed_data['raw_text'],
                file_path=str(file_path)
            )
            db.add(candidate)
            db.commit()
            db.refresh(candidate)
            logger.info(f"Created new candidate: {candidate.id}")
        
        # Generate embedding
        embedding_service = get_embedding_service()
        embedding_text = f"{parsed_data['name']} {' '.join(parsed_data['skills'])} {parsed_data['education']}"
        embedding_vector = embedding_service.generate_embedding(embedding_text)
        
        # Store embedding
        existing_embedding = db.query(Embedding).filter(
            Embedding.candidate_id == candidate.id
        ).first()
        
        if existing_embedding:
            existing_embedding.embedding_vector = embedding_vector
            existing_embedding.model_name = settings.MODEL_NAME
        else:
            embedding = Embedding(
                candidate_id=candidate.id,
                embedding_vector=embedding_vector,
                model_name=settings.MODEL_NAME
            )
            db.add(embedding)
        
        db.commit()
        logger.info(f"Embedding generated for candidate: {candidate.id}")
        
        return candidate
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error uploading resume: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {str(e)}"
        )


@router.post("/job", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def upload_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload and process a job description
    """
    try:
        # Parse job description
        parser = JobParser()
        parsed_data = parser.parse_job_description(job_data.dict())
        
        # Create new job
        job = Job(
            title=parsed_data['title'],
            company=parsed_data['company'],
            description=parsed_data['description'],
            required_skills=parsed_data['required_skills'],
            experience_required=parsed_data['experience_required'],
            location=parsed_data['location'],
            job_type=parsed_data['job_type'],
            seniority_level=parsed_data['seniority_level'],
            domain=parsed_data['domain']
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)
        logger.info(f"Created new job: {job.id}")
        
        # Generate embedding
        embedding_service = get_embedding_service()
        embedding_text = f"{parsed_data['title']} {parsed_data['description']} {' '.join(parsed_data['required_skills'])}"
        embedding_vector = embedding_service.generate_embedding(embedding_text)
        
        # Store embedding
        embedding = Embedding(
            job_id=job.id,
            embedding_vector=embedding_vector,
            model_name=settings.MODEL_NAME
        )
        db.add(embedding)
        db.commit()
        logger.info(f"Embedding generated for job: {job.id}")
        
        return job
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error uploading job: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing job: {str(e)}"
        )
