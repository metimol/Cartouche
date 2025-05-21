from pydantic import BaseModel
from typing import List, Optional

class BotProfile(BaseModel):
    id: Optional[int] = None
    name: str
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    is_bot: bool = True
    prompt: Optional[str] = None
    following: Optional[List[str]] = []
    description: Optional[str] = None
    category: Optional[List[str]] = []
    memory: Optional[dict] = {}
