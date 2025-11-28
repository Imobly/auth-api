from datetime import timedelta
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.src.auth.models import User
from app.src.auth.repository import UserRepository
from app.src.auth.schemas import (
    LoginRequest,
    PasswordChange,
    Token,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.src.auth.security import create_access_token, verify_password


class AuthController:
    """Controller para operações de autenticação"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository()

    def register(self, user_in: UserCreate) -> UserResponse:
        """
        Registrar novo usuário
        ... (same as original)
        """
        constraints = self.repository.check_unique_constraints(
            self.db, user_in.email, user_in.username
        )

        if constraints["email_exists"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado no sistema",
            )

        if constraints["username_exists"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já está em uso",
            )

        user = self.repository.create_user(self.db, user_in)
        return UserResponse.model_validate(user)

    def login(self, login_data: LoginRequest) -> Token:
        user = self.repository.get_by_email_or_username(self.db, login_data.username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(login_data.password, str(user.hashed_password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo",
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=access_token_expires,
        )

        return Token(access_token=access_token, token_type="bearer")

    def get_me(self, current_user: User) -> UserResponse:
        return UserResponse.model_validate(current_user)

    def update_me(self, current_user: User, user_update: UserUpdate) -> UserResponse:
        if user_update.email and user_update.email != current_user.email:
            existing_user = self.repository.get_by_email(self.db, user_update.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado no sistema",
                )

        if user_update.username and user_update.username != current_user.username:
            existing_user = self.repository.get_by_username(self.db, user_update.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username já está em uso",
                )

        updated_user = self.repository.update(self.db, int(current_user.id), user_update)
        return UserResponse.model_validate(updated_user)

    def change_password(self, current_user: User, password_change: PasswordChange) -> dict:
        if not verify_password(password_change.current_password, str(current_user.hashed_password)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha atual incorreta",
            )

        self.repository.update_password(self.db, current_user, password_change.new_password)

        return {"message": "Senha alterada com sucesso"}

    def logout(self, current_user: User) -> dict:
        """
        Logout do usuário.

        Nota: Como usamos JWT stateless, o token continua válido até expirar.
        O cliente deve descartar o token localmente.
        Este endpoint serve para logs/auditoria.
        """
        # Aqui você pode adicionar logs de auditoria se necessário
        # logger.info(f"User {current_user.username} (ID: {current_user.id}) logged out")

        return {
            "message": "Logout realizado com sucesso",
            "detail": "Token será invalidado pelo cliente"
        }

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = self.repository.get_multi(self.db, skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.repository.get(self.db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )
        return UserResponse.model_validate(user)

    def delete_user(self, user_id: int) -> dict:
        user = self.repository.get(self.db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )

        self.repository.remove(self.db, user_id)
        return {"message": "Usuário deletado com sucesso"}
