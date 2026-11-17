from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_cors_origins
from app.database import get_db
from app.routers import restaurant   # ton fichier router
from app.routers import command   
from app.routers import role   
from app.routers import permissions   
from app.routers import product   
from app.routers import user   
from app.routers import restaurant_address
from app.routers import auth
from app.routers import product_pictures
from app.routers import command_lines
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),  # variable CORS_ORIGINS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(restaurant.router)   # on branche ses routes
app.include_router(command.router)
app.include_router(role.router)
app.include_router(permissions.router)
app.include_router(product.router)
app.include_router(user.router)
app.include_router(restaurant_address.router)
app.include_router(auth.router)
app.include_router(product_pictures.router)
app.include_router(command_lines.router)
@app.get("/")
def root():
    return {"message": "Ytasty Crousty API"}


@app.get("/health", tags=["monitoring"])
def health(db: Session = Depends(get_db)):
    """Vérifie que l'API répond et que la base est joignable."""
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(status_code=503, content={"status": "error", "database": "unreachable"})
    return {"status": "ok", "database": "ok"}
