
from pydantic import BaseModel


class RsvpCreate(BaseModel):
    name: str
    email: str
    
    
class RsvpResponse(RsvpCreate):
   pass