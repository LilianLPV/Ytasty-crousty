from fastapi import FastAPI
from app.routers import restaurant   # ton fichier router
from app.routers import command   
from app.routers import role   
from app.routers import permissions   
from app.routers import product   
from app.routers import user   
from app.routers import restaurant_address
from app.routers import auth
from app.routers import product_pictures

app = FastAPI()
app.include_router(restaurant.router)   # on branche ses routes
app.include_router(command.router)
app.include_router(role.router)
app.include_router(permissions.router)
app.include_router(product.router)
app.include_router(user.router)
app.include_router(restaurant_address.router)
app.include_router(auth.router)
app.include_router(product_pictures.router)

@app.get("/")
def root():
    return {"message": "Ytasty Crousty API"}