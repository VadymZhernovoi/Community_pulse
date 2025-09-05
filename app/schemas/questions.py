from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

#

class QuestionBase(BaseModel):
    question: str = Field(..., min_length=1)


class QuestionCreate(QuestionBase):
    category_id: Optional[int] = None
    category: Optional[CategoryBase] = None


class QuestionResponse(QuestionBase):
    id: int
    question: str = Field(..., min_length=10, max_length=100)
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)





