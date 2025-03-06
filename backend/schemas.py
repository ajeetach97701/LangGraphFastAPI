from pydantic import BaseModel
from typing import List



class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str
    
class Fruit(BaseModel):
    name: str
    
class Fruits(BaseModel):
    fruits: List[Fruit]
    