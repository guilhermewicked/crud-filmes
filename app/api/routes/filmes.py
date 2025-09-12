from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import dependencia
from app.db import gets_sets
from app.schemas.filmes import Filme, FilmeCreate

router = APIRouter()

@router.get("/", response_model=List[Filme])
def listar_filmes(
    genero: Optional[str] = Query(None, description="Filtra filmes por genero"), 
    db: Session = Depends(dependencia.get_db)
):
    return gets_sets.get_filmes(db, genero=genero)

@router.post("/", response_model=Filme, status_code=201)
def criar_filme(
    filme: FilmeCreate, 
    db: Session = Depends(dependencia.get_db)
):
    return gets_sets.create_filme(db, filme)

@router.get("/{filme_id}", response_model=Filme)
def obter_filme(
    filme_id: int, 
    db: Session = Depends(dependencia.get_db)
):
    db_filme = gets_sets.get_filme(db, filme_id)
    if db_filme is None:
        raise HTTPException(status_code=404, detail="Filme nao encontrado")
    return db_filme