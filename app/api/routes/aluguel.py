from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import dependencia
from app.db import gets_sets
from app.schemas.aluguel import Aluguel
from app.schemas.filmes import Filme
from app.db.base import Usuario as ModeloUsuario

router = APIRouter()

@router.post("/filmes/{filme_id}/alugar", response_model=Aluguel)
def alugar_unidade_filme(
    filme_id: int, 
    db: Session = Depends(dependencia.get_db), 
    current_user: ModeloUsuario = Depends(dependencia.get_current_user)
):
    db_filme = gets_sets.get_filme(db, filme_id)
    if not db_filme:
        raise HTTPException(status_code=404, detail="Filme nao encontrado")
    if db_filme.unidades == 0:
        raise HTTPException(status_code=400, detail="Nenhuma unidade disponivel para aluguel")
    
    return gets_sets.alugar_filme(db, db_filme, current_user)

@router.get("/", response_model=List[Aluguel])
def listar_filmes_alugados(
    db: Session = Depends(dependencia.get_db), 
    current_user: ModeloUsuario = Depends(dependencia.get_current_user)
):
    return gets_sets.get_alugueis_by_user(db, user_id=current_user.id)

@router.post("/devolver/{aluguel_id}", response_model=Filme)
def devolver_filme_alugado(
    aluguel_id: int, 
    db: Session = Depends(dependencia.get_db),
    current_user: ModeloUsuario = Depends(dependencia.get_current_user)
):
    db_aluguel = gets_sets.get_aluguel(db, aluguel_id)
    if not db_aluguel:
        raise HTTPException(status_code=404, detail="Registro de aluguel nao encontrado")
    
    if db_aluguel.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nao autorizado")
    
    filme_devolvido = gets_sets.devolver_filme(db, db_aluguel)
    return filme_devolvido