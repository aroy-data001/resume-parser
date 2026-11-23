from app.client import client, model
from app.job_description import job_parsed
from app.resume_structure import MatchScore
import json

def final_score1(job_parsed, parsed_resume):
    score_schema = MatchScore.model_json_schema()

    prompt = f"""
    You are an HR recruiter.

    Compare the candidate's resume with the job description.

    JOB DESCRIPTION:
    {job_parsed.model_dump_json(indent=2)}

    CANDIDATE RESUME:
    {parsed_resume.model_dump_json(indent=2)}
    Return JSON matching this schema:

    {score_schema}

    Give me:

    1. Candidate name
    2. Matching skills
    3. Missing important skills
    4. Whether experience requirement is met
    5. Overall match percentage from 0 to 100
    6. A short final verdict

    Keep the response concise and easy to read.
        """
    message = {
        "role": "user",
        "content": prompt
    }
    messages = [message]
    response_format = {
        "type": "json_object"
    }

    response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)

    raw_data = json.loads(response.choices[0].message.content)

    score = MatchScore(**raw_data)

    return score