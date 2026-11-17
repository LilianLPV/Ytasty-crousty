from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.jwt import verify_hash_password, create_access_token


def authentifier(db: Session, username: str, password: str) -> dict:
    user = db.scalars(select(User).where(User.username == username)).first()

    if user is None or not verify_hash_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
        )

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}