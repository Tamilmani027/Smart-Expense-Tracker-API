from datetime import date as date_type
from pydantic import BaseModel, Field, field_validator


class Expense(BaseModel):
    id: int = Field(..., gt=0, description="Unique positive integer identifier")
    title: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(..., gt=0, description="Must be a positive amount")
    category: str = Field(..., min_length=1, max_length=100)
    date: date_type

    @field_validator("title", "category")
    @classmethod
    def not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped