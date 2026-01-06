from pydantic import BaseModel
from typing import List

class ATSKeywords(BaseModel):
    jd_keywords: List[str]          # extracted ONLY from JD
    present_keywords: List[str]     # subset of jd_keywords
    missing_keywords: List[str]     # jd_keywords - present_keywords
    match_score: int

class Experience(BaseModel):
    title: str
    company: str
    bullets: List[str]

class ResumeSchema(BaseModel):
    summary: str
    skills: List[str]
    experience: List[Experience]
    education: List[str]
    ats_keywords: ATSKeywords
