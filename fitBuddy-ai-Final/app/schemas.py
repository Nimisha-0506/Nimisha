from pydantic import BaseModel, Field, field_validator

INTENSITIES = {"low", "medium", "high"}


class UserInput(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    user_id: int = Field(gt=0)
    age: int = Field(ge=10, le=100)
    weight: float = Field(gt=20, le=400)
    goal: str = Field(min_length=2, max_length=200)
    intensity: str

    @field_validator("intensity")
    @classmethod
    def check_intensity(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in INTENSITIES:
            raise ValueError("intensity must be low, medium or high")
        return v


class WorkoutRequest(BaseModel):
    goal: str = Field(min_length=2, max_length=200)
    intensity: str = "medium"


class FeedbackRequest(BaseModel):
    feedback: str = Field(min_length=2, max_length=1000)