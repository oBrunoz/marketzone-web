from pydantic import BaseModel
from typing import Optional

# Schema Pydantic para User
class UserBase(BaseModel):
    username: str
    email: str
    is_active: Optional[bool] = True

# Schema para a criação de um novo User
class UserCreate(UserBase):
    hashed_password: str

# Schema para atualização de User
class UserUpdate(UserBase):
    hashed_password: Optional[str] = None

# Schema Pydantic para User que inclui id e produtos
class User(UserBase):
    id: int
    produtos: Optional[list] = []

    class Config:
        from_attributes = True
