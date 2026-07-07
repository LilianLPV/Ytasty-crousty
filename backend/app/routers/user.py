from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRead
from app.schemas.user import UserCreate
from app.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserRead])
def liste_user(db : Session = Depends(get_db)):
    return db.scalars(select(User)).all()

@router.get("/{id_user}", response_model=UserRead)
def user(id_user: int, db: Session = Depends(get_db)):
    usr = db.get(User, id_user)
    if usr is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return usr

@router.post("/", response_model=UserRead, status_code=201)
def creer_user(data: UserCreate, db: Session = Depends(get_db)):
    usr = User(**data.model_dump())
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr