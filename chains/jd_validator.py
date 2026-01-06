from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace


JD_VALIDATION_PROMPT = """
You are validating whether the following text is a real job description.

Text:
{job_description}

Rules:
- Answer ONLY with "VALID" or "INVALID"
- VALID if it clearly describes a job role, responsibilities, or requirements
- INVALID if it is too short, a greeting, random text, or not a job description
"""

def validate_job_description(job_description: str, llm: ChatHuggingFace) -> bool:
    prompt = PromptTemplate.from_template(JD_VALIDATION_PROMPT)
    response = llm.invoke(prompt.format(job_description=job_description)).content
    return response.strip().upper() == "VALID"
