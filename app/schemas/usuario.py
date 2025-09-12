from pydantic import BaseModel

class UsuarioBase(BaseModel):
    email: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True