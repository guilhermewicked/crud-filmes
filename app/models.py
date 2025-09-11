from sqlalchemy import Column, Integer, String
from app.database import Base

class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    diretor = Column(String, index=True)
    ano = Column(Integer)
    unidades = Column(Integer, default=0)