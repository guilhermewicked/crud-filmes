from pydantic import BaseModel, Field
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
        orm_mode = True
        
        
        
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
        orm_mode = True