import datetime
from pydantic import BaseModel
from .filmes import Filme

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