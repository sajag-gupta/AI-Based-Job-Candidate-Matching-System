"""
Sample data generator for testing the AI Job Matcher
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.database import SessionLocal, Candidate, Job, Embedding
from backend.services import get_embedding_service
from backend.config import get_settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = get_settings()


def create_sample_candidates(db):
    """Create sample candidates"""
    candidates_data = [
        {
            "name": "Alice Johnson",
            "email": "alice.johnson@email.com",
            "phone": "555-0101",
            "skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "Data Analysis", "SQL"],
            "experience_years": 5.0,
            "education": "Master's in Computer Science, Stanford University",
            "raw_text": "Experienced Data Scientist with 5 years of expertise in machine learning, deep learning, and data analysis. Proficient in Python, TensorFlow, PyTorch, and SQL."
        },
        {
            "name": "Bob Smith",
            "email": "bob.smith@email.com",
            "phone": "555-0102",
            "skills": ["JavaScript", "React", "Node.js", "TypeScript", "AWS", "Docker"],
            "experience_years": 4.0,
            "education": "Bachelor's in Software Engineering, MIT",
            "raw_text": "Full Stack Developer with 4 years of experience building scalable web applications using React, Node.js, and cloud technologies."
        },
        {
            "name": "Carol Williams",
            "email": "carol.williams@email.com",
            "phone": "555-0103",
            "skills": ["Python", "FastAPI", "Django", "PostgreSQL", "Redis", "Docker", "Kubernetes"],
            "experience_years": 7.0,
            "education": "Master's in Software Engineering, UC Berkeley",
            "raw_text": "Senior Backend Engineer with 7 years of experience designing and implementing microservices architecture using Python, FastAPI, and cloud-native technologies."
        },
        {
            "name": "David Chen",
            "email": "david.chen@email.com",
            "phone": "555-0104",
            "skills": ["Java", "Spring Boot", "Microservices", "Kafka", "MongoDB", "AWS"],
            "experience_years": 6.0,
            "education": "Bachelor's in Computer Science, Carnegie Mellon",
            "raw_text": "Senior Java Developer with 6 years of experience in enterprise applications, microservices, and distributed systems."
        },
        {
            "name": "Emma Davis",
            "email": "emma.davis@email.com",
            "phone": "555-0105",
            "skills": ["React", "Vue.js", "JavaScript", "CSS", "HTML", "TailwindCSS", "Figma"],
            "experience_years": 3.0,
            "education": "Bachelor's in Design, Rhode Island School of Design",
            "raw_text": "Frontend Developer with 3 years of experience creating beautiful, responsive user interfaces using modern JavaScript frameworks and design tools."
        }
    ]
    
    embedding_service = get_embedding_service()
    
    for data in candidates_data:
        # Check if candidate exists
        existing = db.query(Candidate).filter(Candidate.email == data["email"]).first()
        if existing:
            logger.info(f"Candidate already exists: {data['name']}")
            continue
        
        # Create candidate
        candidate = Candidate(**data)
        db.add(candidate)
        db.flush()
        
        # Generate embedding
        embedding_text = f"{data['name']} {' '.join(data['skills'])} {data['education']}"
        embedding_vector = embedding_service.generate_embedding(embedding_text)
        
        embedding = Embedding(
            candidate_id=candidate.id,
            embedding_vector=embedding_vector,
            model_name=settings.MODEL_NAME
        )
        db.add(embedding)
        
        logger.info(f"Created candidate: {data['name']}")
    
    db.commit()


def create_sample_jobs(db):
    """Create sample jobs"""
    jobs_data = [
        {
            "title": "Senior Machine Learning Engineer",
            "company": "AI Innovations Inc",
            "description": "We are seeking a Senior ML Engineer with expertise in deep learning, PyTorch, and production ML systems. You will lead the development of cutting-edge AI models.",
            "required_skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "AWS"],
            "experience_required": 5.0,
            "location": "San Francisco, CA",
            "job_type": "full-time",
            "seniority_level": "senior",
            "domain": "data_science"
        },
        {
            "title": "Full Stack Developer",
            "company": "WebTech Solutions",
            "description": "Join our team to build modern web applications using React, Node.js, and cloud technologies. Experience with TypeScript and AWS is highly valued.",
            "required_skills": ["React", "Node.js", "JavaScript", "TypeScript", "PostgreSQL", "AWS"],
            "experience_required": 3.0,
            "location": "Remote",
            "job_type": "full-time",
            "seniority_level": "mid",
            "domain": "technology"
        },
        {
            "title": "Backend Python Developer",
            "company": "CloudScale Systems",
            "description": "We need a skilled Python developer to work on our microservices platform. FastAPI, Docker, and Kubernetes experience required.",
            "required_skills": ["Python", "FastAPI", "Docker", "Kubernetes", "PostgreSQL", "Redis"],
            "experience_required": 4.0,
            "location": "Austin, TX",
            "job_type": "full-time",
            "seniority_level": "mid",
            "domain": "technology"
        },
        {
            "title": "Lead Java Architect",
            "company": "Enterprise Tech Corp",
            "description": "Lead the design and implementation of enterprise-scale Java applications using Spring Boot, microservices, and cloud technologies.",
            "required_skills": ["Java", "Spring Boot", "Microservices", "Kafka", "AWS", "MongoDB"],
            "experience_required": 8.0,
            "location": "New York, NY",
            "job_type": "full-time",
            "seniority_level": "senior",
            "domain": "technology"
        },
        {
            "title": "Frontend Developer",
            "company": "Design First Studios",
            "description": "Create stunning user interfaces using React, Vue.js, and modern CSS frameworks. Work closely with designers to implement pixel-perfect designs.",
            "required_skills": ["React", "Vue.js", "JavaScript", "TailwindCSS", "CSS", "HTML"],
            "experience_required": 2.0,
            "location": "Remote",
            "job_type": "full-time",
            "seniority_level": "junior",
            "domain": "technology"
        },
        {
            "title": "Data Scientist",
            "company": "Analytics Pro",
            "description": "Analyze complex datasets and build predictive models using Python, machine learning, and statistical methods. SQL and data visualization skills required.",
            "required_skills": ["Python", "Machine Learning", "SQL", "Pandas", "NumPy", "Tableau"],
            "experience_required": 4.0,
            "location": "Boston, MA",
            "job_type": "full-time",
            "seniority_level": "mid",
            "domain": "data_science"
        }
    ]
    
    embedding_service = get_embedding_service()
    
    for data in jobs_data:
        # Check if job exists
        existing = db.query(Job).filter(
            Job.title == data["title"],
            Job.company == data["company"]
        ).first()
        if existing:
            logger.info(f"Job already exists: {data['title']} at {data['company']}")
            continue
        
        # Create job
        job = Job(**data)
        db.add(job)
        db.flush()
        
        # Generate embedding
        embedding_text = f"{data['title']} {data['description']} {' '.join(data['required_skills'])}"
        embedding_vector = embedding_service.generate_embedding(embedding_text)
        
        embedding = Embedding(
            job_id=job.id,
            embedding_vector=embedding_vector,
            model_name=settings.MODEL_NAME
        )
        db.add(embedding)
        
        logger.info(f"Created job: {data['title']} at {data['company']}")
    
    db.commit()


def main():
    """Generate sample data"""
    logger.info("Generating sample data...")
    
    db = SessionLocal()
    try:
        create_sample_candidates(db)
        create_sample_jobs(db)
        logger.info("Sample data generation completed!")
    except Exception as e:
        logger.error(f"Error generating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
