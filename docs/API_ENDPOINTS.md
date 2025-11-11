# 🔐 Auth API - Documentação dos Endpoints

**Versão:** 0.1.0  
**Base URL:** `http://localhost:8001/api/v1`  
**Autenticação:** JWT Bearer Token  

---

## 📋 Índice

1. [Health Check](#health-check)
2. [Autenticação](#autenticação)
3. [Perfil do Usuário](#perfil-do-usuário)
4. [Administração (Superuser)](#administração-superuser)
5. [Schemas e Validações](#schemas-e-validações)
6. [Códigos de Erro](#códigos-de-erro)
7. [Exemplos de Uso](#exemplos-de-uso)

---

## 🩺 Health Check

### `GET /`
**Descrição:** Verifica se a API está funcionando.

**Autenticação:** ❌ Não requerida

**Response:**
```json
{
  "status": "ok"
}
```

**Exemplo cURL:**
```bash
curl -X GET "http://localhost:8001/"
```

---

## 🔑 Autenticação

### `POST /api/v1/auth/register`
**Descrição:** Registra um novo usuário no sistema.

**Autenticação:** ❌ Não requerida

**Body (JSON):**
```json
{
  "email": "usuario@example.com",
  "username": "meuusername",
  "full_name": "Nome Completo do Usuário",
  "password": "senhaSegura123"
}
```

**Validações:**
- `email`: Formato de email válido (obrigatório)
- `username`: 3-100 caracteres (obrigatório, único)
- `full_name`: Máximo 255 caracteres (opcional)
- `password`: Mínimo 6 caracteres, deve conter pelo menos 1 número e 1 letra (obrigatório)

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "username": "meuusername",
  "full_name": "Nome Completo do Usuário",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-29T22:58:51.781103"
}
```

**Exemplo cURL:**
```bash
curl -X POST "http://localhost:8001/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "usuario@example.com",
       "username": "meuusername", 
       "full_name": "Nome Completo",
       "password": "senhaSegura123"
     }'
```

---

### `POST /api/v1/auth/login`
**Descrição:** Autentica um usuário e retorna um token JWT.

**Autenticação:** ❌ Não requerida

**Body (JSON):**
```json
{
  "username": "meuusername",
  "password": "senhaSegura123"
}
```

**Notas:**
- O campo `username` aceita tanto username quanto email
- Senha deve ter mínimo 6 caracteres

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Token Expires:** 30 minutos (configurável via `ACCESS_TOKEN_EXPIRE_MINUTES`)

**Exemplo cURL:**
```bash
curl -X POST "http://localhost:8001/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "meuusername",
       "password": "senhaSegura123"
     }'
```

---

## 👤 Perfil do Usuário

### `GET /api/v1/auth/me`
**Descrição:** Retorna os dados do usuário logado.

**Autenticação:** ✅ Bearer Token requerido

**Headers:**
```
Authorization: Bearer SEU_TOKEN_JWT
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "username": "meuusername",
  "full_name": "Nome Completo do Usuário",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-29T22:58:51.781103"
}
```

**Exemplo cURL:**
```bash
curl -X GET "http://localhost:8001/api/v1/auth/me" \
     -H "Authorization: Bearer SEU_TOKEN_JWT"
```

---

### `PUT /api/v1/auth/me`
**Descrição:** Atualiza os dados do usuário logado.

**Autenticação:** ✅ Bearer Token requerido

**Headers:**
```
Authorization: Bearer SEU_TOKEN_JWT
Content-Type: application/json
```

**Body (JSON) - Todos os campos são opcionais:**
```json
{
  "email": "novoemail@example.com",
  "username": "novousername",
  "full_name": "Novo Nome Completo",
  "is_active": true
}
```

**Validações:**
- Email e username devem ser únicos (se fornecidos)
- Username: 3-100 caracteres
- Full name: máximo 255 caracteres

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "novoemail@example.com",
  "username": "novousername",
  "full_name": "Novo Nome Completo",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-29T22:58:51.781103"
}
```

**Exemplo cURL:**
```bash
curl -X PUT "http://localhost:8001/api/v1/auth/me" \
     -H "Authorization: Bearer SEU_TOKEN_JWT" \
     -H "Content-Type: application/json" \
     -d '{
       "full_name": "Novo Nome Completo"
     }'
```

---

### `POST /api/v1/auth/change-password`
**Descrição:** Altera a senha do usuário logado.

**Autenticação:** ✅ Bearer Token requerido

**Headers:**
```
Authorization: Bearer SEU_TOKEN_JWT
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "current_password": "senhaAtual123",
  "new_password": "novaSenhaSegura456"
}
```

**Validações:**
- `current_password`: Deve ser a senha atual correta
- `new_password`: Mínimo 6 caracteres, deve conter pelo menos 1 número e 1 letra

**Response (200 OK):**
```json
{
  "message": "Senha alterada com sucesso"
}
```

**Exemplo cURL:**
```bash
curl -X POST "http://localhost:8001/api/v1/auth/change-password" \
     -H "Authorization: Bearer SEU_TOKEN_JWT" \
     -H "Content-Type: application/json" \
     -d '{
       "current_password": "senhaAtual123",
       "new_password": "novaSenhaSegura456"
     }'
```

---

## 👑 Administração (Superuser)

> ⚠️ **Atenção:** Os endpoints abaixo requerem privilégios de superuser.

### `GET /api/v1/auth/users`
**Descrição:** Lista todos os usuários do sistema (paginado).

**Autenticação:** ✅ Bearer Token requerido (Superuser)

**Headers:**
```
Authorization: Bearer SEU_TOKEN_ADMIN
```

**Query Parameters:**
- `skip` (int, optional): Número de registros a pular (default: 0)
- `limit` (int, optional): Limite de registros retornados (default: 100)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "email": "usuario1@example.com",
    "username": "usuario1",
    "full_name": "Usuario Um",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2025-10-29T22:58:51.781103"
  },
  {
    "id": 2,
    "email": "admin@example.com",
    "username": "admin",
    "full_name": "Administrator",
    "is_active": true,
    "is_superuser": true,
    "created_at": "2025-10-29T22:59:26.466402"
  }
]
```

**Exemplo cURL:**
```bash
curl -X GET "http://localhost:8001/api/v1/auth/users?skip=0&limit=10" \
     -H "Authorization: Bearer SEU_TOKEN_ADMIN"
```

---

### `GET /api/v1/auth/users/{user_id}`
**Descrição:** Retorna os dados de um usuário específico pelo ID.

**Autenticação:** ✅ Bearer Token requerido (Superuser)

**Headers:**
```
Authorization: Bearer SEU_TOKEN_ADMIN
```

**Path Parameters:**
- `user_id` (int): ID do usuário

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "username": "meuusername",
  "full_name": "Nome Completo",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-29T22:58:51.781103"
}
```

**Exemplo cURL:**
```bash
curl -X GET "http://localhost:8001/api/v1/auth/users/1" \
     -H "Authorization: Bearer SEU_TOKEN_ADMIN"
```

---

### `DELETE /api/v1/auth/users/{user_id}`
**Descrição:** Remove um usuário do sistema.

**Autenticação:** ✅ Bearer Token requerido (Superuser)

**Headers:**
```
Authorization: Bearer SEU_TOKEN_ADMIN
```

**Path Parameters:**
- `user_id` (int): ID do usuário a ser removido

**Response (200 OK):**
```json
{
  "message": "Usuário deletado com sucesso"
}
```

**Exemplo cURL:**
```bash
curl -X DELETE "http://localhost:8001/api/v1/auth/users/1" \
     -H "Authorization: Bearer SEU_TOKEN_ADMIN"
```

---

## 📝 Schemas e Validações

### UserCreate
```json
{
  "email": "string (EmailStr, obrigatório)",
  "username": "string (3-100 chars, obrigatório)",
  "full_name": "string (max 255 chars, opcional)",
  "password": "string (6-100 chars, obrigatório, deve ter número + letra)"
}
```

### UserUpdate
```json
{
  "email": "string (EmailStr, opcional)",
  "username": "string (3-100 chars, opcional)",
  "full_name": "string (max 255 chars, opcional)",
  "password": "string (6-100 chars, opcional)",
  "is_active": "boolean (opcional)"
}
```

### LoginRequest
```json
{
  "username": "string (username ou email, obrigatório)",
  "password": "string (min 6 chars, obrigatório)"
}
```

### PasswordChange
```json
{
  "current_password": "string (min 6 chars, obrigatório)",
  "new_password": "string (min 6 chars, obrigatório, deve ter número + letra)"
}
```

### UserResponse
```json
{
  "id": "int",
  "email": "string",
  "username": "string",
  "full_name": "string|null",
  "is_active": "boolean",
  "is_superuser": "boolean",
  "created_at": "datetime (ISO format)"
}
```

### Token
```json
{
  "access_token": "string (JWT)",
  "token_type": "string (sempre 'bearer')"
}
```

---

## ⚠️ Códigos de Erro

### 400 Bad Request
```json
{
  "detail": "Email já cadastrado no sistema"
}
```
```json
{
  "detail": "Username já está em uso"
}
```
```json
{
  "detail": "Senha atual incorreta"
}
```

### 401 Unauthorized
```json
{
  "detail": "Credenciais inválidas",
  "headers": {"WWW-Authenticate": "Bearer"}
}
```
```json
{
  "detail": "Não foi possível validar as credenciais",
  "headers": {"WWW-Authenticate": "Bearer"}
}
```

### 403 Forbidden
```json
{
  "detail": "Usuário inativo"
}
```
```json
{
  "detail": "Usuário não possui privilégios suficientes"
}
```

### 404 Not Found
```json
{
  "detail": "Usuário não encontrado"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "password"],
      "msg": "Senha deve conter pelo menos um número",
      "input": "senhasemdigito"
    }
  ]
}
```

---

## 🚀 Exemplos de Uso

### Fluxo Completo com PowerShell

```powershell
# 1. Health Check
Invoke-RestMethod -Uri "http://localhost:8001/" -Method Get

# 2. Registrar usuário
$registerBody = @{
    email = "teste@example.com"
    username = "teste123"
    full_name = "Usuario Teste"
    password = "senha123"
} | ConvertTo-Json

$newUser = Invoke-RestMethod -Uri "http://localhost:8001/api/v1/auth/register" -Method Post -Body $registerBody -ContentType "application/json"

# 3. Login
$loginBody = @{
    username = "teste123"
    password = "senha123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "http://localhost:8001/api/v1/auth/login" -Method Post -Body $loginBody -ContentType "application/json"
$token = $loginResponse.access_token

# 4. Obter dados do usuário
$headers = @{Authorization = "Bearer $token"}
$userData = Invoke-RestMethod -Uri "http://localhost:8001/api/v1/auth/me" -Method Get -Headers $headers

# 5. Alterar senha
$passwordChangeBody = @{
    current_password = "senha123"
    new_password = "novasenha456"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/api/v1/auth/change-password" -Method Post -Body $passwordChangeBody -ContentType "application/json" -Headers $headers
```

### Fluxo Admin com PowerShell

```powershell
# Promover usuário a admin no banco (via Docker)
docker exec -it auth-api-postgres-1 psql -U postgres -d auth_db -c "UPDATE users SET is_superuser = true WHERE username = 'admin';"

# Login como admin
$adminLoginBody = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$adminResponse = Invoke-RestMethod -Uri "http://localhost:8001/api/v1/auth/login" -Method Post -Body $adminLoginBody -ContentType "application/json"
$adminToken = $adminResponse.access_token

# Listar todos os usuários
$adminHeaders = @{Authorization = "Bearer $adminToken"}
$allUsers = Invoke-RestMethod -Uri "http://localhost:8001/api/v1/auth/users" -Method Get -Headers $adminHeaders

# Obter usuário específico
$specificUser = Invoke-RestMethod -Uri "http://localhost:8001/api/v1/auth/users/1" -Method Get -Headers $adminHeaders

# Deletar usuário
Invoke-RestMethod -Uri "http://localhost:8001/api/v1/auth/users/1" -Method Delete -Headers $adminHeaders
```

---

## 🔧 Configuração

### Variáveis de Ambiente
```env
DATABASE_URL=postgresql://postgres:admin123@postgres:5432/auth_db
SECRET_KEY=sua-chave-secreta-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=false
```

### Executar API
```bash
# Com Docker Compose
docker-compose up -d --build

# A API estará disponível em http://localhost:8001
```

---

**📚 Documentação Interativa:**
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`