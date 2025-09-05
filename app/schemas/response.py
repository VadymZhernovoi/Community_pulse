from pydantic import BaseModel, Field


class ResponseCreate(BaseModel):
    question_id: int = Field(..., description='Question ID')
    is_agree: bool = Field(..., description='Is Agree?')


class StaticResponse(BaseModel):
    question_id: int = Field(..., description='Question ID')
    agree_count: int = Field(..., ge=0, description='Agree Count')
    disagree_count: int = Field(..., ge=0, description='Disagree Count')

class MessageResponse(BaseModel):
    id: int
    message: str = Field(..., min_length=10, max_length=100)