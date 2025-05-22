# Projeto: Sistema de Matrículas com FastAPI para SUTHUB

Este projeto implementa uma API de matrículas com FastAPI, autenticação via Basic Auth, persistência de dados em MongoDB, e processamento assíncrono via serviço dedicado.

## 🛠 Tecnologias Utilizadas

* Python 3.11
* FastAPI
* MongoDB (cloud via string no .env)
* Docker + Docker Compose
* Pytest + httpx

---

## 📁 Estrutura do Projeto

```
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── routes/
│   │   ├── age_groups.py
│   │   └── enrollments.py
│   └── models/
│	│	├── age_group_in_out.py
│   │   ├── enrollment_request.py
│   │   └── enrollment_status.py
│   ├── static/
│   │   │-- images/
│   │       │-- suthub-banner.PNG
│   │
│	├── services/
│   │	└── enrollment_processor.py
│   │-- templates/
│   │   │-- index.html
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
├── .dockerignore
└── README.md

```

---

## ⚙️ Configuração

### 1. Crie o arquivo `.env`

Exemplo:

```env
BASIC_AUTH_USERNAME=admin
BASIC_AUTH_PASSWORD=1234
MONGO_URI=mongodb+srv://<usuário>:<senha>@<cluster>.mongodb.net/?retryWrites=true&w=majority

#Se quiser, pode usar o endereço: mongodb+srv://admin:test1234!@cluster0.qg6itmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

> Use a string de conexão do MongoDB cloud (Atlas, por exemplo) para testes persistentes.

---

## ▶️ Como Executar Localmente

### 1. Suba os serviços com Docker Compose:

```terminal
docker-compose up --build
```

### 2. Acesse a extensão MongoDB do vscode e procure a opção:
```
Connect with Connection String

A seguir, pedirá para você inserir a conexão com o banco MongoDB, nesse caso, poderá inserir e clicar Enter:
mongodb+srv://admin:test1234!@cluster0.qg6itmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

### 3. Acesse a página inicial do projeto:
```
http://localhost:8000/
```

### 4. Acesse a documentação interativa:

```
http://localhost:8000/docs
```

Clique em **Authorize** e insira:

* Usuário: `admin`
* Senha: `1234`

---

## 📡 Endpoints Principais

### Age Groups (Protegido)

* `POST /age-groups`: cria novo grupo de idade
* `GET /age-groups`: lista todos os grupos
* `DELETE /age-groups/{id}`: deleta grupo

### Enrollments

* `POST /enrollments`: registra uma matrícula
* `GET /enrollments/enroll/{cpf}`: consulta status da matrícula (autenticado)

### Processor

* Serviço separado que processa as matrículas pendentes e atualiza o status após 2 segundos

---



---

## ✅ Requisitos Atendidos

✔️ Cadastro de grupos de idade
✔️ Matrícula validando idade
✔️ Status consultado por CPF
✔️ Processador assíncrono com espera de 2s
✔️ Autenticação via Basic Auth
✔️ MongoDB persistente usando `.env`

---

## 📬 Contato

Para dúvidas ou sugestões, entre em contato com Luiz Felipe.
Linkedin: https://www.linkedin.com/in/luiz-felipe-dev-python/
