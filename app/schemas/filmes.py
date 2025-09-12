from pydantic import BaseModel, Field

class FilmeBase(BaseModel):
    titulo: str
    diretor: str
    ano: int
    unidades: int = Field(default=1, ge=0)
    genero: str

class FilmeCreate(FilmeBase):
    pass

class Filme(FilmeBase):
    id: int

    class Config:
        from_attributes = True