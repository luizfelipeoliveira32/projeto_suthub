# projeto_suthub
Teste de nivelamento técnico passado pela Suthub onde foi criado uma aplicação FAST API usando MongoDB e Docker

# 🚀 Comandos para rodar o projeto

🔨 1. Build da imagem Docker
No diretório raiz do projeto, execute:

```bash
docker build -t minha-api .
```

🧱 2. Rodar o container

```bash
docker run -d -p 8000:8000 minha-api
```

✅ 3. Verificar se está rodando

```bash
docker ps
```

Você verá algo como:

```bash
CONTAINER ID   IMAGE       COMMAND                  PORTS                    NAMES
xxxxxxxxxxxx   minha-api   "uvicorn main:app ..."   0.0.0.0:8000->8000/tcp   nome_aleatorio
```

🌐 4. Acessar no navegador

API em funcionamento: http://localhost:8000

Documentação automática: http://localhost:8000/docs

