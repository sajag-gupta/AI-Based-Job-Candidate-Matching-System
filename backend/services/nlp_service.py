"""
NLP Service for text processing and feature extraction
"""
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class NLPService:
    """Natural Language Processing utilities"""
    
    # Common skill keywords
    COMMON_SKILLS = {
        'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
        'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'sql',
        'postgresql', 'mysql', 'mongodb', 'redis', 'docker', 'kubernetes',
        'aws', 'azure', 'gcp', 'git', 'ci/cd', 'agile', 'scrum', 'html', 'css',
        'rest api', 'graphql', 'microservices', 'machine learning', 'deep learning',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'data analysis',
        'tableau', 'power bi', 'spark', 'hadoop', 'linux', 'bash', 'devops',
        'jenkins', 'terraform', 'ansible', 'elasticsearch', 'kafka', 'rabbitmq',
        'c++', 'c#', '.net', 'php', 'ruby', 'go', 'rust', 'scala', 'kotlin',
        'swift', 'objective-c', 'android', 'ios', 'flutter', 'react native'
    }
    
    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """
        Extract skills from text using keyword matching
        """
        text_lower = text.lower()
        found_skills = []
        
        for skill in NLPService.COMMON_SKILLS:
            # Use word boundaries for accurate matching
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    @staticmethod
    def extract_experience_years(text: str) -> float:
        """
        Extract years of experience from text
        """
        # Patterns like "5 years", "3+ years", "5-7 years"
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)',
            r'(?:experience|exp)(?:\s+of)?\s+(\d+)\+?\s*(?:years?|yrs?)',
            r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                if isinstance(matches[0], tuple):
                    # Range found, take average
                    return (int(matches[0][0]) + int(matches[0][1])) / 2
                else:
                    return float(matches[0])
        
        return 0.0
    
    @staticmethod
    def extract_email(text: str) -> str:
        """
        Extract email address from text
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else ""
    
    @staticmethod
    def extract_phone(text: str) -> str:
        """
        Extract phone number from text
        """
        phone_patterns = [
            r'\+?1?\s*\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})',
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                if isinstance(matches[0], tuple):
                    return ''.join(matches[0])
                return matches[0]
        
        return ""
    
    @staticmethod
    def classify_seniority(text: str, experience_years: float) -> str:
        """
        Classify job/candidate seniority level
        """
        text_lower = text.lower()
        
        # Keyword-based classification
        if any(word in text_lower for word in ['senior', 'lead', 'principal', 'staff', 'architect']):
            return 'senior'
        elif any(word in text_lower for word in ['junior', 'entry', 'graduate', 'intern']):
            return 'junior'
        elif any(word in text_lower for word in ['mid-level', 'intermediate', 'associate']):
            return 'mid'
        
        # Experience-based classification
        if experience_years >= 7:
            return 'senior'
        elif experience_years >= 3:
            return 'mid'
        else:
            return 'junior'
    
    @staticmethod
    def classify_domain(text: str) -> str:
        """
        Classify job domain/industry
        """
        text_lower = text.lower()
        
        domain_keywords = {
            'technology': ['software', 'developer', 'engineer', 'programmer', 'tech', 'it', 'devops'],
            'data_science': ['data scientist', 'machine learning', 'ai', 'analytics', 'data engineer'],
            'finance': ['finance', 'banking', 'investment', 'trading', 'fintech'],
            'healthcare': ['healthcare', 'medical', 'hospital', 'clinical', 'pharmaceutical'],
            'marketing': ['marketing', 'digital marketing', 'seo', 'content', 'brand'],
            'sales': ['sales', 'business development', 'account manager'],
            'design': ['designer', 'ui/ux', 'graphic', 'creative'],
            'operations': ['operations', 'logistics', 'supply chain', 'project manager']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return domain
        
        return 'general'
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()
    
    @staticmethod
    def calculate_skill_overlap(skills1: List[str], skills2: List[str]) -> Dict:
        """
        Calculate skill overlap between two skill lists
        """
        set1 = set([s.lower() for s in skills1])
        set2 = set([s.lower() for s in skills2])
        
        overlap = set1.intersection(set2)
        overlap_percentage = (len(overlap) / len(set2) * 100) if set2 else 0
        
        return {
            'overlapping_skills': list(overlap),
            'overlap_count': len(overlap),
            'overlap_percentage': round(overlap_percentage, 2),
            'missing_skills': list(set2 - set1)
        }
