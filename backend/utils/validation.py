from pydantic import BaseModel, validator, ValidationError
from typing import Literal

class FileMeta(BaseModel):
    filename: str
    content_type: Literal["image/jpeg", "image/png", "application/pdf", "text/plain"]
    size: int  # in bytes

    @validator("size")
    def size_limit(cls, v):
        max_size = 5 * 1024 * 1024  # 5MB
        if v > max_size:
            raise ValueError("File size exceeds 5MB limit.")
        return v
