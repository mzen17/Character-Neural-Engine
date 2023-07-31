from pydantic import BaseModel
from typing import Optional

class MessageRequest (BaseModel):
    message: str
    id: int
    character: str
    session: Optional[str] = None
    person_asking: Optional[str] = None
    key: Optional[str] = None
