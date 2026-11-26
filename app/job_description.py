
import json

from groq.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
)
from pydantic import BaseModel, Field

from app.client import client, model


class JobD(BaseModel):
    role: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    minimum_education: str
    minimum_experience: str | None = None
    responsibilities: str


job_schema = JobD.model_json_schema()

response_format = {
    "type": "json_object"
}


def parse_job_description(job_description: str) -> JobD:
    """Extract structured information from a dynamic job description."""

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    system_prompt = f"""
    You are an expert HR assistant.

    Analyze job descriptions and extract structured information.

    Return ONLY valid JSON matching this schema:

    {job_schema}

    IMPORTANT:
    Do NOT return the schema itself.
    Do NOT return fields like "properties", "title" or "type".
    Fill the schema with actual information extracted from the job description.

    If minimum experience is not mentioned, return null.
    If information for a list is missing, return an empty list.
    Do not invent information.
    """

    user_prompt = f"""
    Analyze the following job description:

    {job_description}
    """

    sys_msg: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": system_prompt
    }

    user_msg: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": user_prompt
    }

    messages = [sys_msg, user_msg]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format=response_format
    )

    answer = response.choices[0].message.content

    if not answer:
        raise ValueError("The LLM returned an empty response.")

    raw_json = json.loads(answer)

    job_parsed = JobD(**raw_json)

    return job_parsed