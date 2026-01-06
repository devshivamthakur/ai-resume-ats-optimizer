from pydantic import BaseModel, Field
from typing import List

class Experience(BaseModel):
    title: str
    company: str
    bullets: List[str]

class ATSKeywords(BaseModel):
    jd_keywords: List[str] = Field(
        description="Important keywords and phrases extracted from the job description"
    )
    present_keywords: List[str] = Field(
        description="Keywords from the job description that appear in or are clearly implied by the resume"
    )
    missing_keywords: List[str] = Field(
        description="Important job description keywords missing from the resume"
    )

class ResumeSchema(BaseModel):
    summary: str
    skills: List[str]
    experience: List[Experience]
    education: List[str]
    ats_keywords: ATSKeywords
