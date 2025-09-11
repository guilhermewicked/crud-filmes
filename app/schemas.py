from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

class FilmeBase(BaseModel):
    titulo: str
    diretor: str
    ano: int
    unidades: int = Field(default=1, ge=0)
    gênero: str

class FilmeCreate(FilmeBase):
    pass

class Filme(FilmeBase):
    id: int

    class Config:
        from_attributes = True
        
        
        
#aluguel:
class AluguelBase(BaseModel):
    filme_id: int

class AluguelCreate(AluguelBase):
    pass

class Aluguel(AluguelBase):
    id: int
    data_aluguel: datetime.datetime
    filme: Filme

    class Config:
        from_attributes = True
        
class UsuarioBase(BaseModel):
    email: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None