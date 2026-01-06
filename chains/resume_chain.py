import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from schemas.resume_schema import ResumeSchema

load_dotenv()


llm_endpoint = HuggingFaceEndpoint(
    repo_id=os.getenv("CHAT_HF_MODEL"),
    task="text-generation",
    temperature=0,
    max_new_tokens=1200,
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_TOKEN"),
)

llm = ChatHuggingFace(llm=llm_endpoint)


parser = PydanticOutputParser(pydantic_object=ResumeSchema)


def run_resume_chain(resume: str, job_description: str | None = None) -> ResumeSchema:

    if job_description:
        template = open("prompts/job_specific.txt").read()
        prompt = PromptTemplate(
            template=template,
            input_variables=["resume", "job_description"],
            partial_variables={
                "format_instructions": parser.get_format_instructions()
            },
        )
        inputs = {
            "resume": resume,
            "job_description": job_description,
        }
    else:
        template = open("prompts/general.txt").read()
        prompt = PromptTemplate(
            template=template,
            input_variables=["resume"],
            partial_variables={
                "format_instructions": parser.get_format_instructions()
            },
        )
        inputs = {"resume": resume}

    chain = prompt | llm | parser

    return chain.invoke(inputs)
