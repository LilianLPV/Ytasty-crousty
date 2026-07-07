from sqlalchemy.orm import Session
from app.models.base import engine

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()