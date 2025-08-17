from pydantic import BaseModel, Field
from typing import List, Optional

class Job(BaseModel):
    title: str = Field(..., example="Data Scientist")
    company: str = Field(..., example="TCS")
    location: str = Field(..., example="Hyderabad")
    description: Optional[str] = Field(None, example="ML project experience needed")
    skills_required: List[str] = Field(..., example=["Python", "ML", "NLP"])
    posted_date: Optional[str] = Field(None, example="2025-08-15")
    link: Optional[str] = Field(None, example="https://company.com/job/123")
