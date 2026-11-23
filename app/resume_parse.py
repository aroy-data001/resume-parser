from app.client import client, model
from app.resume_structure import resume_schema, Resume
import json
def resumeParse(resume_text):
    sys_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

    Return ONLY valid JSON matching this schema:

    {resume_schema}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.
    """
    user_prompt = f"""
    Read the resume text here {resume_text} and fit it for {resume_schema} as per
    the system instructions.
    """

    sys_msg = {
        "role": "system",
        "content": sys_prompt
    }

    user_msg = {
        "role": "user",
        "content": user_prompt
    }

    messages = [sys_msg, user_msg]

    response_format = {
        "type": "json_object"
    }

    response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)

    raw_data = json.loads(response.choices[0].message.content)
    parsed_resume = Resume(**raw_data)
    return parsed_resume
