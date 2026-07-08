from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.database import get_db
from app.utils.jwt import verify_hash_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalars(
        select(User).where(User.username == form_data.username)
    ).first()

    if user is None or not verify_hash_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"
        )
    
    access_token = create_access_token({"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
