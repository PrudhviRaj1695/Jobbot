from pydantic import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    name: str = Field(..., example="Alice")
    email: Optional[str] = Field(None, example="alice@email.com")
    skills: List[str] = Field(..., example=["Python", "ML"])
    preferences: Optional[List[str]] = Field(None, example=["Remote", "Full-time"])
    telegram_chat_id: Optional[str] = Field(None, example="1514304895")
