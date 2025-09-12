from sqlalchemy.orm import Session
from typing import Optional

from app.db.base import Filme, Aluguel, Usuario
from app.schemas.filmes import FilmeCreate
from app.schemas.usuario import UsuarioCreate
# ANTES: from app.core.security import get_password_hash
# AGORA:
from app.security.auth import get_password_hash

def get_filmes(db: Session, genero: Optional[str] = None):
    query = db.query(Filme)
    if genero:
        query = query.filter(Filme.genero.ilike(f"%{genero}%"))
    return query.all()

def get_filme(db: Session, filme_id: int):
    return db.query(Filme).filter(Filme.id == filme_id).first()

def get_aluguel(db: Session, aluguel_id: int):
    return db.query(Aluguel).filter(Aluguel.id == aluguel_id).first()

def get_alugueis(db: Session):
    return db.query(Aluguel).all()

def get_alugueis_by_user(db: Session, user_id: int):
    return db.query(Aluguel).filter(Aluguel.usuario_id == user_id).all()

def get_user_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def count_filmes(db: Session) -> int:
    return db.query(Filme).count()

def create_filme(db: Session, filme: FilmeCreate):
    db_filme = Filme(**filme.dict())
    db.add(db_filme)
    db.commit()
    db.refresh(db_filme)
    return db_filme

def create_user(db: Session, user: UsuarioCreate):
    hashed_password = get_password_hash(user.password)
    db_user = Usuario(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def alugar_filme(db: Session, filme: Filme, user: Usuario):
    if filme and filme.unidades > 0:
        filme.unidades -= 1
        db_aluguel = Aluguel(filme_id=filme.id, usuario_id=user.id)
        db.add(db_aluguel)
        db.commit()
        db.refresh(filme)
        db.refresh(db_aluguel)
        return db_aluguel
    return None

def devolver_filme(db: Session, aluguel: Aluguel):
    aluguel.filme.unidades += 1
    db.delete(aluguel)
    db.commit()
    return aluguel.filme