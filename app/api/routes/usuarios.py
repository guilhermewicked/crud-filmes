from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import dependencia
from app.db import gets_sets
from app.schemas.usuario import Usuario, UsuarioCreate
from app.schemas.token import Token
from app.security import auth
from app.db.base import Usuario as ModeloUsuario

router = APIRouter()

@router.post("/", response_model=Usuario)
def create_user(
    user: UsuarioCreate, 
    db: Session = Depends(dependencia.get_db)
):
    db_user = gets_sets.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return gets_sets.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login_for_access_token(
    db: Session = Depends(dependencia.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = gets_sets.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=Usuario)
def read_users_me(
    current_user: ModeloUsuario = Depends(dependencia.get_current_user)
):
    return current_user