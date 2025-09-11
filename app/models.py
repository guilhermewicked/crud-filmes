from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    diretor = Column(String, index=True)
    ano = Column(Integer)
    unidades = Column(Integer, default=0)
    gênero = Column(String, index=True)
    alugueis = relationship("Aluguel", back_populates="filme")
    #relação 