from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, crud, database

#create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="CRUD Filmes API")

# DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/filmes", response_model=list[schemas.Filme])
def listar_filmes(db: Session = Depends(get_db)):
    return crud.get_filmes(db)

@app.post("/filmes", response_model=schemas.Filme)
def criar_filme(filme: schemas.FilmeCreate, db: Session = Depends(get_db)):
    return crud.create_filme(db, filme)

@app.get("/filmes/{filme_id}", response_model=schemas.Filme)
def obter_filme(filme_ed: int, db: Session = Depends(get_db)):
    db_movie = crud.get_filme(db, filme_ed)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie