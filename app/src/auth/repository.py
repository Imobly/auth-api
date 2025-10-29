from typing import Optional

from sqlalchemy.orm import Session

from app.db.base_repository import BaseRepository
from app.src.auth.models import User
from app.src.auth.schemas import UserCreate, UserUpdate
from app.src.auth.security import get_password_hash


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_by_email_or_username(self, db: Session, identifier: str) -> Optional[User]:
        return (
            db.query(User)
            .filter((User.email == identifier) | (User.username == identifier))
            .first()
        )

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        user_data = user_in.model_dump(exclude={"password"})
        user_data["hashed_password"] = get_password_hash(user_in.password)

        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    def update_password(self, db: Session, user: User, new_password: str) -> User:
        hashed_password: str = get_password_hash(new_password)
        user.hashed_password = hashed_password  # type: ignore[assignment]
        db.commit()
        db.refresh(user)

        return user

    def check_unique_constraints(self, db: Session, email: str, username: str) -> dict:
        email_exists = self.get_by_email(db, email) is not None
        username_exists = self.get_by_username(db, username) is not None

        return {"email_exists": email_exists, "username_exists": username_exists}

    def update(self, db: Session, user_id: int, obj_in: UserUpdate) -> User:  # type: ignore[override]
        db_obj = self.get(db, user_id)
        if db_obj is None:
            raise ValueError(f"User with id {user_id} not found")
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, user_id: int) -> User:
        return self.delete(db, id=user_id)
