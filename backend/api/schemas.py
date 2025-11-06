"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
from datetime import datetime


# Auth Schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "recruiter"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Candidate Schemas
class CandidateCreate(BaseModel):
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]
    skills: List[str]
    experience_years: float
    education: str
    raw_text: str


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    experience_years: float
    education: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Job Schemas
class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    required_skills: List[str]
    experience_required: float
    location: str = "Remote"
    job_type: str = "full-time"
    seniority_level: Optional[str]
    domain: Optional[str]


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    description: str
    required_skills: List[str]
    experience_required: float
    location: str
    job_type: str
    seniority_level: Optional[str]
    domain: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Match Schemas
class MatchResponse(BaseModel):
    candidate_id: Optional[int]
    job_id: Optional[int]
    candidate_name: Optional[str]
    job_title: Optional[str]
    company: Optional[str]
    similarity_score: float
    skill_overlap: Dict
    
    class Config:
        from_attributes = True


class MatchRequest(BaseModel):
    candidate_id: Optional[int]
    job_id: Optional[int]
    top_k: int = Field(default=10, ge=1, le=100)
    min_similarity: float = Field(default=0.5, ge=0.0, le=1.0)


# Search Schemas
class SearchRequest(BaseModel):
    query: Optional[str]
    skills: Optional[List[str]]
    min_experience: Optional[float]
    max_experience: Optional[float]
    job_type: Optional[str]
    location: Optional[str]
    seniority_level: Optional[str]


# Error Schema
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str]
    correlation_id: Optional[str]
