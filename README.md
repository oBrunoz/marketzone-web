# Projeto de API Web MarketZone

## Introdução
Este é o README do projeto de API web **Market Zone**, desenvolvido para a disciplina **Desenvolvimento de Sistemas Web**. A API é uma ferramenta para gerenciar produtos e o carrinho de compras de um e-commerce fictício. Permite operações como cadastro de produtos, adição de produtos ao carrinho, visualização do carrinho e finalização de compras. Além disso, possui funcionalidades de autenticação e perfil de usuário.

## Funcionalidades
- **Cadastro de Produtos**: Permite o cadastro de novos produtos com informações detalhadas como nome, descrição, preço, categoria, avaliação e imagem.
- **Gerenciamento de Carrinho de Compras**: Os usuários podem adicionar produtos ao carrinho, visualizar os itens no carrinho, remover itens e finalizar a compra.
- **Autenticação de Usuário**: Controle de acesso para garantir que apenas usuários autenticados possam realizar certas operações, como adicionar produtos ao carrinho ou realizar compras.
- **Gerenciamento de Usuários**: Possibilita o cadastro, login, logout, visualização e atualização de perfil de usuário.

## Requisitos
- **Python 3.8+**: Linguagem de programação utilizada para o desenvolvimento da API.
- **FastAPI**: Framework web moderno e rápido para a criação da API.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Jinja2**: Motor de template utilizado para renderização de páginas HTML.
- **SQLite**: Banco de dados utilizado para armazenamento de dados.
- **Passlib**: Biblioteca para hashing de senhas.
- **Shutil**: Biblioteca para manipulação de arquivos, utilizada para salvar imagens.

## Instalação

### Requisitos pré-requisitos
Certifique-se de que você tem o Python 3.8 ou superior instalado no seu ambiente.

### Instalação da API

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/VictorBoccucci/marketzone-web.git
   ```
2. **Navegue até o diretório do projeto**:
   ```bash
   cd projeto-api-web
   ```
3. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/MacOS
   venv\Scripts\activate  # Para Windows
   ```
4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Inicie o servidor**:
   ```bash
   uvicorn src.main:app --reload
   ```

## Uso da API

### Endpoints

- **Rota Principal - Home**:
  - **GET /**: Exibe a página inicial com a listagem de produtos disponíveis.

- **Gerenciamento de Produtos**:
  - **GET /produto/cadastro**: Exibe a página de cadastro de produtos.
  - **POST /produto/cadastro**: Processa o cadastro de um novo produto.
  - **POST /produto/add-to-cart**: Adiciona um produto ao carrinho.
  - **GET /produto/carrinho**: Exibe o carrinho de compras.
  - **POST /produto/carrinho/deletar**: Remove um item do carrinho.
  - **POST /produto/carrinho/comprar**: Finaliza a compra dos itens no carrinho.

- **Gerenciamento de Usuários**:
  - **GET /cadastro**: Exibe a página de cadastro de usuários.
  - **POST /cadastro**: Processa o cadastro de um novo usuário.
  - **GET /login**: Exibe a página de login de usuários.
  - **POST /logar**: Processa o login do usuário.
  - **GET /logout**: Realiza o logout do usuário.
  - **GET /profile**: Exibe a página de perfil do usuário.
  - **POST /update_profile**: Atualiza os dados do perfil do usuário.

### Parâmetros

- **Cadastro de Produto**:
  - `nome`: Nome do produto (string, obrigatório).
  - `descricao`: Descrição do produto (string, opcional).
  - `preco`: Preço do produto (string, obrigatório, no formato "R$ 0,00").
  - `categoria`: Categoria do produto (string, obrigatório).
  - `rating`: Avaliação do produto (inteiro, opcional).
  - `imagem`: Imagem do produto (arquivo, opcional).
  - `user_id`: ID do usuário (inteiro, obtido da sessão).

- **Adição ao Carrinho**:
  - `product_id`: ID do produto a ser adicionado (inteiro, obrigatório).

- **Remoção de Item do Carrinho**:
  - `item_id`: ID do item a ser removido (inteiro, obrigatório).

- **Finalização da Compra**:
  - `total_price`: Preço total dos itens no carrinho (float, obrigatório).

- **Cadastro de Usuário**:
  - `username`: Nome de usuário (string, obrigatório).
  - `email`: Endereço de email (string, obrigatório).
  - `hashed_password`: Senha criptografada (string, obrigatório).

- **Login de Usuário**:
  - `email`: Endereço de email (string, obrigatório).
  - `hashed_password`: Senha criptografada (string, obrigatório).

- **Atualização de Perfil**:
  - `username`: Nome de usuário (string, obrigatório).
  - `email`: Endereço de email (string, obrigatório).
  - `password`: Nova senha (string, opcional).

### Exemplos de Uso

1. **Cadastro de Produto**:
   ```http
   POST /produto/cadastro
   {
       "nome": "Camisa Polo",
       "descricao": "Camisa Polo de alta qualidade",
       "preco": "R$ 49,99",
       "categoria": "Roupas",
       "rating": 5,
       "imagem": <arquivo de imagem>
   }
   ```

2. **Adicionar Produto ao Carrinho**:
   ```http
   POST /produto/add-to-cart
   {
       "product_id": 1
   }
   ```

3. **Visualizar Carrinho**:
   ```http
   GET /produto/carrinho
   ```

4. **Remover Item do Carrinho**:
   ```http
   POST /produto/carrinho/deletar
   {
       "item_id": 1
   }
   ```

5. **Finalizar Compra**:
   ```http
   POST /produto/carrinho/comprar
   {
       "total_price": 149.99
   }
   ```

6. **Cadastro de Usuário**:
   ```http
   POST /cadastro
   {
       "username": "johndoe",
       "email": "johndoe@example.com",
       "hashed_password": "supersecretpassword"
   }
   ```

7. **Login de Usuário**:
   ```http
   POST /logar
   {
       "email": "johndoe@example.com",
       "hashed_password": "supersecretpassword"
   }
   ```

8. **Atualização de Perfil**:
   ```http
   POST /update_profile
   {
       "username": "johnsmith",
       "email": "johnsmith@example.com",
       "password": "newpassword"
   }
   ```

## Testes

- **Teste de Cadastro de Produto**: Verificar se a rota `/produto/cadastro` permite o cadastro de novos produtos com todos os campos obrigatórios e opcionais.
- **Teste de Adição ao Carrinho**: Validar se a função de adicionar produtos ao carrinho está incrementando a quantidade corretamente e atualizando a sessão.
- **Teste de Finalização de Compra**: Confirmar se a compra é finalizada com sucesso e o estoque dos produtos é atualizado adequadamente.
- **Teste de Cadastro de Usuário**: Verificar se a rota `/cadastro` permite o cadastro de novos usuários com todos os campos obrigatórios.
- **Teste de Login de Usuário**: Validar se a função de login autentica corretamente os usuários e cria a sessão.
- **Teste de Atualização de Perfil**: Confirmar se a rota `/update_profile` permite a atualização dos dados do usuário autenticado.

## Contribuição

- **[Nome do Contribuidor 1]**: Responsável pelo desenvolvimento inicial e configuração do projeto.
- **[Nome do Contribuidor 2]**: Auxiliou na implementação das funcionalidades de carrinho de compras e finalização de compra.
- **[Nome do Contribuidor 3]**: Implementou as rotas de cadastro de produto e auxiliou nos testes da API.
- **[Nome do Contribuidor 4]**: Desenvolveu as funcionalidades de autenticação de usuário e gerenciamento de perfil.
