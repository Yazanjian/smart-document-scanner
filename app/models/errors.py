from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    error: str
    message: Optional[str] = None
