# auth-api

Microservice de autenticação para Imobly

- Endpoints: `/api/v1/auth/*`
- Emite JWTs (HS256)
- Postgres como banco de dados

Setup de ambiente e execução

Consulte o guia de ambientes para entender DEV, HML e PROD e como alternar:

- Documentação: https://imobly.github.io/Documentation/guides/environments/

Setup local (com Docker):

1. Configure `.env` (use o template `.env.example`). O projeto usa um seletor de ambiente via `ENVIRONMENT` e três DSNs:

```
# Seletor de ambiente
ENVIRONMENT=staging               # development|staging|production

# DSNs por ambiente
DATABASE_URL_DEV=postgresql://user:pass@host:6543/db?sslmode=require
DATABASE_URL_HML=postgresql://user:pass@host:6543/db?sslmode=require
DATABASE_URL_PROD=postgresql://user:pass@host:6543/db?sslmode=require

# Configurações de segurança
SECRET_KEY=generate-a-secure-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,https://demo.imobly.com
```

```
DATABASE_URL=postgresql://postgres:admin123@postgres:5432/auth_db
SECRET_KEY=generate-a-secure-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

2. Subir com docker-compose:

```powershell
cd Auth-api
# Desenvolvimento (usa HML por padrão)
docker compose -f docker-compose.yml up -d --build
# Produção
docker compose -f docker-compose.prod.yml up -d --build
```

3. API estará em http://localhost:8001 (ou porta configurada)

Integração com `Backend` (stateless JWT):

- Use o mesmo `SECRET_KEY` em `Backend` para validar tokens localmente.
- No `Backend`, defina `AUTH_SERVICE_URL` e `SECRET_KEY` nas variáveis de ambiente.

Referências úteis:

- Ambientes e variáveis: https://imobly.github.io/Documentation/guides/environments/
- Swagger local: http://localhost:8001/docs

Push para GitHub:

1. Crie o repositório `auth-api` na organização Imobly
2. No diretório `Auth-api` local:

```powershell
git init
git add .
git commit -m "chore: initial auth-api scaffold"
git remote add origin https://github.com/Imobly/auth-api.git
git branch -M main
git push -u origin main
```

Depois de push, configure secrets no GitHub: `SECRET_KEY` e configurações do CI.
