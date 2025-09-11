from sqlalchemy.orm import Session
from app import models, schemas

def get_filmes(db: Session):
    return db.query(models.Filme).all()

def get_filme(db: Session, filme_id: int):
    return db.query(models.Filme).filter(models.Filme.id == filme_id).first()

def create_filme(db: Session, filme: schemas.FilmeCreate):
    db_filme = models.Filme(
        titulo=filme.titulo,
        diretor=filme.diretor,
        ano=filme.ano
        
    )
    db.add(db_filme)
    db.commit()
    db.refresh(db_filme)
    return db_filme