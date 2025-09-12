from fastapi import FastAPI


from app.api.routes import filmes, usuarios, aluguel
from app.db.base import Base
from app.db.database import engine, SessionLocal
from app.db import gets_sets
from app.schemas.filmes import FilmeCreate

#populate
#usar p debug
def populate_database():
    db = SessionLocal()
    try:
        if gets_sets.count_filmes(db) == 0:
            # se o banco está vazio, popula com lista base
            filmes_iniciais = [
                FilmeCreate(titulo="Dune Part Two", diretor="Denis Villeneuve", ano=2024, unidades=3, genero="Ficcao Cientifica"),
                FilmeCreate(titulo="Poor Things", diretor=" Yorgos Lanthimos", ano=2023, unidades=5, genero="Comedia Fantasia"),
                FilmeCreate(titulo="A Origem", diretor="Christopher Nolan", ano=2010, unidades=8, genero="Ficcao Cientifica"),
                FilmeCreate(titulo="Bastardos Inglorios", diretor="Quentin Tarantino", ano=2009, unidades=7, genero="Acao"),
                FilmeCreate(titulo="O Senhor dos Aneis: O Retorno do Rei", diretor="Peter Jackson", ano=2003, unidades=6, genero="Aventura"),
                FilmeCreate(titulo="Flow", diretor="Gints Zilbalodis", ano=2024, unidades=4, genero="Animacao"),
            ]
            for filme in filmes_iniciais:
                gets_sets.create_filme(db, filme)
            print("Povoamento OK.")
            # listagem = gets_sets.get_filmes(db)
        else:
            #debug
            print("Banco ja povoado, operacao cancelada.")
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

#populate
populate_database()

app = FastAPI(
    title="Movie Rental API",
    description="An API designed to manage a movie rental system with user authentication and movie inventory management.",
    version="2.0.0"
)

# colocar firebase aqui, configurar social login google, github.

app.include_router(filmes.router, prefix="/filmes", tags=["Filmes"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["User & Auth"])
app.include_router(aluguel.router, prefix="/api/alugueis", tags=["Rental Operations"])