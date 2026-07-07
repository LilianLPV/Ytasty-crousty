from fastapi import FastAPI
from app.routers import restaurant   # ton fichier router
from app.routers import command   # ton fichier router
from app.routers import role   # ton fichier router
from app.routers import permissions   # ton fichier router
from app.routers import product   # ton fichier router
from app.routers import user   # ton fichier router
from app.routers import restaurant_address
app = FastAPI()
app.include_router(restaurant.router)   # on branche ses routes
app.include_router(command.router)
app.include_router(role.router)
app.include_router(permissions.router)
app.include_router(product.router)
app.include_router(user.router)
app.include_router(restaurant_address.router)

@app.get("/")
def root():
    return {"message": "Ytasty Crousty API"}