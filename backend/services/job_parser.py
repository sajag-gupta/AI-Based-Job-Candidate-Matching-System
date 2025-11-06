"""
Job Description Parser Service
"""
import logging
from typing import Dict

from backend.services.nlp_service import NLPService

logger = logging.getLogger(__name__)


class JobParser:
    """Service for parsing job descriptions"""
    
    def __init__(self):
        self.nlp_service = NLPService()
    
    def parse_job_description(self, job_data: Dict) -> Dict:
        """
        Parse job description and extract structured information
        """
        try:
            title = job_data.get('title', '')
            description = job_data.get('description', '')
            
            # Combine title and description for analysis
            full_text = f"{title} {description}"
            
            # Extract information
            required_skills = self.nlp_service.extract_skills(full_text)
            experience_required = self.nlp_service.extract_experience_years(description)
            seniority_level = self.nlp_service.classify_seniority(full_text, experience_required)
            domain = self.nlp_service.classify_domain(full_text)
            
            # Extract job type
            job_type = self._extract_job_type(description)
            
            return {
                'title': title,
                'company': job_data.get('company', 'Not specified'),
                'description': description,
                'required_skills': required_skills,
                'experience_required': experience_required,
                'location': job_data.get('location', 'Remote'),
                'job_type': job_type,
                'seniority_level': seniority_level,
                'domain': domain
            }
        
        except Exception as e:
            logger.error(f"Error parsing job description: {e}")
            raise
    
    def _extract_job_type(self, text: str) -> str:
        """
        Extract job type (full-time, part-time, contract, etc.)
        """
        text_lower = text.lower()
        
        if 'full-time' in text_lower or 'full time' in text_lower:
            return 'full-time'
        elif 'part-time' in text_lower or 'part time' in text_lower:
            return 'part-time'
        elif 'contract' in text_lower or 'contractor' in text_lower:
            return 'contract'
        elif 'freelance' in text_lower:
            return 'freelance'
        elif 'intern' in text_lower:
            return 'internship'
        else:
            return 'full-time'  # Default
