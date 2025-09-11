from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional # ALTERADO
from app import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Movies API",
    description="API focused on managing a movie rental service.",
    version="1.0.0"
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# rotas filme

@app.get("/filmes", response_model=List[schemas.Filme], tags=["Filmes"])
def listar_filmes(genero: Optional[str] = Query(None, description="Filtra filmes por gênero"), db: Session = Depends(get_db)):

    return crud.get_filmes(db, genero=genero)

@app.post("/filmes", response_model=schemas.Filme, status_code=201, tags=["Filmes"])
def criar_filme(filme: schemas.FilmeCreate, db: Session = Depends(get_db)):

    return crud.create_filme(db, filme)

@app.get("/filmes/{filme_id}", response_model=schemas.Filme, tags=["Filmes"])
def obter_filme(filme_id: int, db: Session = Depends(get_db)):

    db_filme = crud.get_filme(db, filme_id)
    if db_filme is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return db_filme

# rotas aluguel

@app.post("/filmes/alugar/{filme_id}", response_model=schemas.Filme, tags=["Aluguel"])
def alugar_unidade_filme(filme_id: int, db: Session = Depends(get_db)):

    db_filme = crud.get_filme(db, filme_id)
    if not db_filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    if db_filme.unidades == 0:
        raise HTTPException(status_code=400, detail="Nenhuma unidade disponível para aluguel")
    
    filme_atualizado = crud.alugar_filme(db, db_filme)
    return filme_atualizado

@app.get("/alugueis", response_model=List[schemas.Aluguel], tags=["Aluguel"])
def listar_filmes_alugados(db: Session = Depends(get_db)):
    return crud.get_alugueis(db)

@app.post("/devolver/{aluguel_id}", response_model=schemas.Filme, tags=["Aluguel"])
def devolver_filme_alugado(aluguel_id: int, db: Session = Depends(get_db)):

    db_aluguel = crud.get_aluguel(db, aluguel_id)
    if not db_aluguel:
        raise HTTPException(status_code=404, detail="Registro de aluguel não encontrado")
    
    filme_devolvido = crud.devolver_filme(db, db_aluguel)
    return filme_devolvido