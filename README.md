#####

Guia Rapido de Execucao e Uso
Este guia mostra como iniciar a aplicação e testar as funcionalidades principais.

-> Pre-requisitos:

-> Git
-> Docker + compose

-> Como Rodar o Projeto:
-> 1. Clone o repositorio para a sua maquina (git clone).
-> 2. Abra um terminal na pasta raiz do projeto (crud-filmes).
-> 3. Execute o comando: docker compose up --build e aguarde o Docker iniciar os containers.
-> 5. A API estara no ar em: http://localhost:8000
-> 6. A documentacao interativa estara em: http://localhost:8000/docs

-> Fluxo de teste:
-> 0. Abrir documentacao interativa: http://localhost:8000/docs

-> 1. Crie uma conta:
--> Na documentacao, use a rota POST /api/usuarios/ para registrar um email e senha.


-> 2. Faca Login para obter o Token:
--> Use a rota POST /api/usuarios/token.
--> Preencha os campos username (com seu email) e password.
--> Copie o access_token da resposta (Opcional)

-> 3. Autorize-se na Documentacao:
--> Clique no botao "Authorize" no topo da pagina.
--> Na janela, cole seu token no campo "Value" no formato: Bearer <token> (opcional)
--> Faça login da conta criada
--> Clique em "Authorize" e feche a janela. O cadeado ficara fechado, agora voce esta autenticado.

-> 4. Teste as Operacoes:
--> Agora voce esta autenticado.
--> Use a rota POST /api/alugueis/filmes/{filme_id}/alugar para alugar um filme.
--> Use a rota GET /api/alugueis/ para ver seus alugueis.
--> Use a rota POST /api/alugueis/devolver/{aluguel_id} para devolver um filme.