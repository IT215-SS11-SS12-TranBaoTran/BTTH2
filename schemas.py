from pydantic import BaseModel, Field
from typing import Optional, Any

class SmartHomeRequest(BaseModel):
    plan_code: str
    plan_name: str
    device_quantity: int = Field(gt=0)
    price: float = Field(gt=0)

class ResponseModel(BaseModel):
    statusCode: int
    message: str
    error: Optional[Any]
    data: Optional[Any]
    path: str
    timestamp: str
