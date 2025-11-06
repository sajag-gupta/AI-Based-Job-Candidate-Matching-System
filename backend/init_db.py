"""
Database initialization and seed script
"""
import sys
from pathlib import Path

# Add backend to Python path
sys.path.append(str(Path(__file__).parent.parent))

from backend.database import init_db, SessionLocal, User, Candidate, Job
from backend.core.security import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_users(db):
    """Seed initial users"""
    users = [
        {
            "email": "admin@jobmatcher.com",
            "password": "admin123",
            "full_name": "Admin User",
            "role": "admin"
        },
        {
            "email": "recruiter@jobmatcher.com",
            "password": "recruiter123",
            "full_name": "Recruiter User",
            "role": "recruiter"
        }
    ]
    
    for user_data in users:
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if not existing:
            # Ensure password is bytes and within bcrypt limit
            password = user_data["password"][:72]
            user = User(
                email=user_data["email"],
                hashed_password=get_password_hash(password),
                full_name=user_data["full_name"],
                role=user_data["role"]
            )
            db.add(user)
            logger.info(f"Created user: {user_data['email']}")
    
    db.commit()


def seed_sample_jobs(db):
    """Seed sample job postings"""
    sample_jobs = [
        {
            "title": "Senior Python Developer",
            "company": "TechCorp Inc",
            "description": "We are looking for an experienced Python developer with expertise in FastAPI, Django, and machine learning. Must have 5+ years of experience.",
            "required_skills": ["Python", "FastAPI", "Django", "Machine Learning", "SQL", "Docker"],
            "experience_required": 5.0,
            "location": "San Francisco, CA",
            "job_type": "full-time",
            "seniority_level": "senior",
            "domain": "technology"
        },
        {
            "title": "Full Stack Engineer",
            "company": "StartupXYZ",
            "description": "Join our team as a Full Stack Engineer. Work with React, Node.js, and PostgreSQL to build scalable web applications.",
            "required_skills": ["React", "Node.js", "JavaScript", "PostgreSQL", "AWS"],
            "experience_required": 3.0,
            "location": "Remote",
            "job_type": "full-time",
            "seniority_level": "mid",
            "domain": "technology"
        },
        {
            "title": "Data Scientist",
            "company": "DataAI Solutions",
            "description": "Seeking a data scientist with strong Python, machine learning, and deep learning skills. Experience with TensorFlow and PyTorch required.",
            "required_skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy"],
            "experience_required": 4.0,
            "location": "New York, NY",
            "job_type": "full-time",
            "seniority_level": "mid",
            "domain": "data_science"
        }
    ]
    
    for job_data in sample_jobs:
        existing = db.query(Job).filter(
            Job.title == job_data["title"],
            Job.company == job_data["company"]
        ).first()
        
        if not existing:
            job = Job(**job_data)
            db.add(job)
            logger.info(f"Created job: {job_data['title']} at {job_data['company']}")
    
    db.commit()


def main():
    """Initialize database and seed data"""
    logger.info("Initializing database...")
    init_db()
    
    logger.info("Seeding database...")
    db = SessionLocal()
    try:
        seed_users(db)
        seed_sample_jobs(db)
        logger.info("Database seeding completed successfully!")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
