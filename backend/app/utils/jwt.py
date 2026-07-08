import os
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

# Charge le .env
load_dotenv()

# Configuration JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"       
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuration du hachage des mdp
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Transforme un mdp en hash
def hash_password(password):
    return pwd_context.hash(password)

# Vérifie le mdp hash correspond au mdp du début
def verify_hash_password(password, hashed):
    return pwd_context.verify(password, hashed)

# Génère un token JWT avec une expiration de 30 minutes
def create_access_token(data: dict):
    to_encode = data.copy()
    
    # Calcule de l'expiration par rapport a l'heure acutelle
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # On encode le contenu avec la clé secrète
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return  encoded_jwt

# On définit le point d'entrée pour l'authentifcation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Fonction pour protéger les routes d'un utilisateur non connecté
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Une erreur si le token est invalide
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
    )
    try:
        # On tente de décoder et de vérifier la signature du token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # On extrait le nom de l'utilisateur
        username = payload.get("sub") # sub = identifiant
        if username is None:
            raise credentials_exception
    except JWTError:
        # Si y a un problème sur le token alors renvoie l'erreur
        raise credentials_exception

    # Vérification de l'utilisateur dans la bdd pour savoir s'il existe
    user = db.scalars(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    # Si tout est bon on retourne l'objet utilisateur
    return user