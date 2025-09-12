#####
```Resumo```

Este repositorio contem a aplicacao do desafio de CRUD filmes utilizando FAST API, docker, sqlalchemy,

Tambem esta contida no repositorio uma experimentacao com a tecnologia do framework ODOO com o objetivo de oferecer uma alternativa de resolucao ao desafio com o framework, com auxilio do github copilot.

```Guia Rapido de Execucao e Uso (FASTAPI+SQLALCHEMY)```

Este guia mostra como iniciar a aplicação e testar as funcionalidades principais.

```Pre-requisitos:```

-> **Git**: Necessario para clonar o repositorio para a sua maquina.
   -->[https://git-scm.com/book/pt-br/v2/Come%C3%A7ando-Instalando-o-Git](https://git-scm.com/book/pt-br/v2/Come%C3%A7ando-Instalando-o-Git)

-> **Docker + Compose**: Necessario para construir e executar a aplicacao em container. O Docker Compose tambem deve ser instalado, embora ja venha incluso na maioria das instalacoes docker desktop.
   -->[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)


```Como Rodar o Projeto:```

1. Clone/download do repositorio para a sua maquina.

2. Abra um terminal na pasta raiz do projeto.

3. Execute o comando: docker compose up --build e aguarde o Docker iniciar os containers.

4. A API estara no ar em: http://localhost:8000

5. A documentacao interativa estara em: http://localhost:8000/docs

```Fluxo de teste:```

0. Abrir documentacao interativa: http://localhost:8000/docs

1. Crie uma conta:
Na documentacao, use a rota POST /api/usuarios/ para registrar um email e senha.


2. Faca Login para obter o Token:
Use a rota POST /api/usuarios/token.

Preencha os campos username (com seu email) e password.

Copie o access_token da resposta (Opcional)


3. Autorizar a documentacao:

Clique no botao "Authorize" no topo da pagina.

Na janela, cole seu token no campo "Value" no formato: Bearer <token> (opcional)

```Faça login da conta criada```

Preencha com o cadastro utilizado para login

Clique em "Authorize" e feche a janela. O cadeado ficara fechado, agora voce esta autenticado.

4. Teste as Operacoes:

--> Use a rota POST /api/alugueis/filmes/{filme_id}/alugar para alugar um filme.

--> Use a rota GET /api/alugueis/ para ver seus alugueis.

--> Use a rota POST /api/alugueis/devolver/{aluguel_id} para devolver um filme.


```ODOO```

-> Inicie o ambiente Odoo com o comando: docker compose -f docker-compose.odoo.yml up -d

-> interface web no navegador em: http://localhost:8069

-> crie a base de dados (ex: nome 'locadora_db', senha 'admin').

-> Ative o developer mode no menu de 'Definicoes'.



```nao habilitado (ODOO):```

  -> No menu 'App', clique em 'Atualizar Lista de Apliсаcoes'.

  -> Remova o filtro 'Apliсаcoes' da barra de pesquisa e procure por 'Odoo Movie CRUD' para o instalar.

  -> Teste a listagem de filmes com um pedido GET para: http://localhost:8069/api/filmes

  -> Crie um novo filme com um pedido POST para a mesma URL, enviando o JSON do filme no corpo da requisição.

```planejamento de melhorias: ```

1 - filtros de pesquisa (filmes: + de 1 genero, )

2 - implementacao ODOO framework e comparacao 

3 - login firebase - Social Login

4 - correcao de sessao/autenticacao pelo oAuth.

