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

def create_filme(db: Session, filme: schemas.FilmeCreate):
    db_filme = models.Filme(**filme.dict())
    db.add(db_filme)
    db.commit()
    db.refresh(db_filme)
    return db_filme


def alugar_filme(db: Session, filme: models.Filme):
    if filme and filme.unidades > 0:
        filme.unidades -= 1
        db_aluguel = models.Aluguel(filme_id=filme.id)
        db.add(db_aluguel)
        db.commit()
        db.refresh(filme)
        return filme
    return None

def get_aluguel(db: Session, aluguel_id: int):
    return db.query(models.Aluguel).filter(models.Aluguel.id == aluguel_id).first()

def devolver_filme(db: Session, aluguel: models.Aluguel):
    aluguel.filme.unidades += 1
    db.delete(aluguel)
    db.commit()
    return aluguel.filme

def get_alugueis(db: Session):
    return db.query(models.Aluguel).all()