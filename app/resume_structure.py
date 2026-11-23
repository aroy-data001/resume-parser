from pydantic import BaseModel

class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    skills: list[str] = []
    duration: float | None = None
    responsibility: str | None = None

class Resume(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    total_education: list[str] = []
    total_experience: list[Experience] = []
    total_skills: list[str] = []
    total_duration: float | None = None

resume_schema = Resume.model_json_schema()

class MatchScore(BaseModel):
    score: int
    details: list[str]

