from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from jose import JWTError, jwt

from app import models, schemas, crud, database, security


#populate
#usar p debug
def populate_database():

    db = database.SessionLocal()
    try:
        if crud.count_filmes(db) == 0:
            # se o banco está vazio, popula com lista base
            filmes_iniciais = [
                schemas.FilmeCreate(titulo="Dune Part Two", diretor="Denis Villeneuve", ano=2024, unidades=3, genero="Ficção Científica"),
                schemas.FilmeCreate(titulo="Poor Things", diretor=" Yorgos Lanthimos", ano=2023, unidades=5, genero="Comédia Fantasia"),
                schemas.FilmeCreate(titulo="A Origem", diretor="Christopher Nolan", ano=2010, unidades=8, genero="Ficção Científica"),
                schemas.FilmeCreate(titulo="Bastardos Inglórios", diretor="Quentin Tarantino", ano=2009, unidades=7, genero="Ação"),
                schemas.FilmeCreate(titulo="O Senhor dos Anéis: O Retorno do Rei", diretor="Peter Jackson", ano=2003, unidades=6, genero="Aventura"),
                schemas.FilmeCreate(titulo="Flow", diretor="Gints Zilbalodis", ano=2024, unidades=4, genero="Animação"),
            ]
            for filme in filmes_iniciais:
                crud.create_filme(db, filme)
            print("Povoamento OK.")
           # listagem = crud.get_filmes(db)
        else:
            #debug
            print("Banco já povoado, operação cancelada.")
    finally:
        db.close()


models.Base.metadata.create_all(bind=database.engine)

#populate
populate_database()

app = FastAPI(
    title="Movie Rental API",
    description="An API designed to manage a movie rental system with user authentication and movie inventory management.",
    version="1.0.0"
)

# auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# colocar firebase aqui, configurar social login google, github.

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# auth and user routes

@app.post("/token", response_model=schemas.Token, tags=["Auth"])
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):

    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/usuarios", response_model=schemas.Usuario, tags=["User"])
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/usuarios/me", response_model=schemas.Usuario, tags=["User"])
def read_users_me(current_user: models.Usuario = Depends(get_current_user)):
    return current_user

# movie routes

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

# rental routes

@app.post("/filmes/alugar/{filme_id}", response_model=schemas.Aluguel, tags=["Aluguel"])
def alugar_unidade_filme(filme_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    db_filme = crud.get_filme(db, filme_id)
    if not db_filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    if db_filme.unidades == 0:
        raise HTTPException(status_code=400, detail="Nenhuma unidade disponível para aluguel")
    
    return crud.alugar_filme(db, db_filme, current_user)

@app.get("/alugueis", response_model=List[schemas.Aluguel], tags=["Aluguel"])
def listar_filmes_alugados(db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    return crud.get_alugueis_by_user(db, user_id=current_user.id)


@app.post("/devolver/{aluguel_id}", response_model=schemas.Filme, tags=["Aluguel"])
def devolver_filme_alugado(aluguel_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    db_aluguel = crud.get_aluguel(db, aluguel_id)
    if not db_aluguel:
        raise HTTPException(status_code=404, detail="Registro de aluguel não encontrado")
    
   
    if db_aluguel.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    
    filme_devolvido = crud.devolver_filme(db, db_aluguel)
    return filme_devolvido