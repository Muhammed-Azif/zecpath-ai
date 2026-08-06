from pydantic import BaseModel
from fastapi import UploadFile

class ScoreRequest(BaseModel):
    skills_score: float
    experience_score: float
    education_score: float
    semantic_score: float


class ShortlistRequest(BaseModel):
    overall_score: float
    threshold: float = 70

class ParseRequest(BaseModel):
    file_path: str