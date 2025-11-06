"""
Resume Parser Service for extracting information from PDF/DOCX files
"""
import logging
from typing import Dict
import PyPDF2
import docx
from pathlib import Path

from backend.services.nlp_service import NLPService

logger = logging.getLogger(__name__)


class ResumeParser:
    """Service for parsing resume files"""
    
    def __init__(self):
        self.nlp_service = NLPService()
    
    def parse_file(self, file_path: str) -> Dict:
        """
        Parse resume file and extract information
        """
        try:
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.pdf':
                text = self._extract_text_from_pdf(file_path)
            elif file_extension in ['.docx', '.doc']:
                text = self._extract_text_from_docx(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            return self._parse_resume_text(text)
        
        except Exception as e:
            logger.error(f"Error parsing resume file: {e}")
            raise
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise
    
    def _extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            raise
    
    def _parse_resume_text(self, text: str) -> Dict:
        """
        Parse resume text and extract structured information
        """
        try:
            # Clean text
            text = self.nlp_service.clean_text(text)
            
            # Extract information
            name = self._extract_name(text)
            email = self.nlp_service.extract_email(text)
            phone = self.nlp_service.extract_phone(text)
            skills = self.nlp_service.extract_skills(text)
            experience_years = self.nlp_service.extract_experience_years(text)
            education = self._extract_education(text)
            
            return {
                'name': name,
                'email': email,
                'phone': phone,
                'skills': skills,
                'experience_years': experience_years,
                'education': education,
                'raw_text': text
            }
        
        except Exception as e:
            logger.error(f"Error parsing resume text: {e}")
            raise
    
    def _extract_name(self, text: str) -> str:
        """
        Extract candidate name from resume text
        (Usually the first non-empty line)
        """
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) < 100:  # Name should be relatively short
                # Check if it looks like a name (not email, phone, etc.)
                if '@' not in line and not any(char.isdigit() for char in line):
                    return line
        return "Unknown"
    
    def _extract_education(self, text: str) -> str:
        """
        Extract education information
        """
        education_keywords = ['education', 'degree', 'university', 'college', 
                            'bachelor', 'master', 'phd', 'diploma']
        
        lines = text.lower().split('\n')
        education_section = []
        in_education = False
        
        for line in lines:
            if any(keyword in line for keyword in education_keywords):
                in_education = True
            elif in_education and len(education_section) > 0:
                # Stop at next section
                if any(word in line for word in ['experience', 'skills', 'projects', 'certifications']):
                    break
            
            if in_education and line.strip():
                education_section.append(line.strip())
        
        return ' | '.join(education_section[:5]) if education_section else "Not specified"
