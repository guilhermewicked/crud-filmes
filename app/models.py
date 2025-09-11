from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean # Adicionar Boolean
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
    
class Aluguel(Base):
    __tablename__ = "alugueis"

    id = Column(Integer, primary_key=True, index=True)
    data_aluguel = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    filme_id = Column(Integer, ForeignKey("filmes.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    filme = relationship("Filme", back_populates="alugueis")
    usuario = relationship("Usuario", back_populates="alugueis")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    alugueis = relationship("Aluguel", back_populates="usuario")
    