from pydantic import BaseModel
from typing import Optional

class SuccessResponse(BaseModel):
    status: str

class ErrorResponse(BaseModel):
    status: str
    message: Optional[str] = None
