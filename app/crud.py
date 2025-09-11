from sqlalchemy.orm import Session
from app import models, schemas
from typing import Optional

def get_filmes(db: Session, genero: Optional[str] = None):
    query = db.query(models.Filme)
    if genero:
        query = query.filter(models.Filme.gênero.ilike(f"%{genero}%"))
    return query.all()

def get_filme(db: Session, filme_id: int):
    return db.query(models.Filme).filter(models.Filme.id == filme_id).first()

def get_aluguel(db: Session, aluguel_id: int):
    return db.query(models.Aluguel).filter(models.Aluguel.id == aluguel_id).first()

def get_alugueis(db: Session):
    return db.query(models.Aluguel).all()

def get_alugueis_by_user(db: Session, user_id: int):
    return db.query(models.Aluguel).filter(models.Aluguel.usuario_id == user_id).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def count_filmes(db: Session) -> int:
    return db.query(models.Filme).count()

def create_filme(db: Session, filme: schemas.FilmeCreate):
    db_filme = models.Filme(**filme.dict())
    db.add(db_filme)
    db.commit()
    db.refresh(db_filme)
    return db_filme

def create_user(db: Session, user: schemas.UsuarioCreate):
    from app.security import get_password_hash
    hashed_password = get_password_hash(user.password)
    db_user = models.Usuario(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def alugar_filme(db: Session, filme: models.Filme, user: models.Usuario):
    if filme and filme.unidades > 0:
        filme.unidades -= 1
        db_aluguel = models.Aluguel(filme_id=filme.id, usuario_id=user.id)
        db.add(db_aluguel)
        db.commit()
        db.refresh(filme)
        db.refresh(db_aluguel)
        return db_aluguel
    return None

def devolver_filme(db: Session, aluguel: models.Aluguel):
    aluguel.filme.unidades += 1
    db.delete(aluguel)
    db.commit()
    return aluguel.filme