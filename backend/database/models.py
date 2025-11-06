"""
SQLAlchemy ORM models for PostgreSQL
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.connection import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="recruiter")  # recruiter, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Candidate(Base):
    """Candidate profile model"""
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(50))
    skills = Column(JSON)  # List of skills
    experience_years = Column(Float)
    education = Column(Text)
    raw_text = Column(Text)  # Full parsed resume text
    file_path = Column(String(500))  # Path to uploaded resume
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    embeddings = relationship("Embedding", back_populates="candidate", cascade="all, delete-orphan")
    match_results = relationship("MatchResult", back_populates="candidate", cascade="all, delete-orphan")


class Job(Base):
    """Job posting model"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255))
    description = Column(Text, nullable=False)
    required_skills = Column(JSON)  # List of required skills
    experience_required = Column(Float)  # Years of experience
    location = Column(String(255))
    job_type = Column(String(50))  # full-time, part-time, contract
    seniority_level = Column(String(50))  # junior, mid, senior, lead
    domain = Column(String(100))  # tech, finance, healthcare, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    embeddings = relationship("Embedding", back_populates="job", cascade="all, delete-orphan")
    match_results = relationship("MatchResult", back_populates="job", cascade="all, delete-orphan")


class Embedding(Base):
    """Vector embeddings storage"""
    __tablename__ = "embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=True)
    embedding_vector = Column(JSON, nullable=False)  # Store as JSON array
    model_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    candidate = relationship("Candidate", back_populates="embeddings")
    job = relationship("Job", back_populates="embeddings")


class MatchResult(Base):
    """Candidate-Job match results"""
    __tablename__ = "match_results"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    similarity_score = Column(Float, nullable=False, index=True)
    skill_overlap = Column(JSON)  # Overlapping skills
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    candidate = relationship("Candidate", back_populates="match_results")
    job = relationship("Job", back_populates="match_results")
