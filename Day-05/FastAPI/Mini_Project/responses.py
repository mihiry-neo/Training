from pydantic import BaseModel

class UserSummaryResponse(BaseModel):
    message:str
    details: dict