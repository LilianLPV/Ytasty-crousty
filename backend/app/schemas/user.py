import re
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.schemas.role import RoleRead

class UserRead(BaseModel):
    # Grâce a sa Pydantic peut lire un objet de SQLAchemy et vérifier 
    model_config = ConfigDict(from_attributes=True)

    id_user: int
    name: str
    first_name: str
    username: str
    id_restaurant: int | None = None

#POST
class UserCreate(BaseModel):
    
    name: str
    first_name: str
    username: str = Field(min_length=8, max_length=12)
    password: str = Field(min_length=12, max_length=64)
    id_role: int
    id_restaurant: int | None = None


    @field_validator("username")
    @classmethod
    def valider_username(cls, valeur):
        if valeur is None:
            return valeur
        if not valeur.isalnum():
            raise ValueError("L'identifiant doit contenir unique des lettres et des chiffres")
        return valeur
    
    @field_validator("password")
    @classmethod
    def valider_password(cls, valeur):
        
        if valeur is None:
            return valeur
        if not re.search(r"[A-Z]", valeur):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")
        if not re.search(r"[0-9]", valeur):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")
        if not re.search(r"[^A-Za-z0-9]", valeur):
            raise ValueError("Le mot de passe doit contenir au moins un caractère spécial")
        return valeur  

#PUT

class UserUpdate(BaseModel):
    
    name: str | None = None
    first_name: str | None = None
    username: str | None = Field(default=None, min_length=8, max_length=12)
    password: str | None = Field(default=None, min_length=12, max_length=64)
    id_role: int | None = None
    id_restaurant: int | None = None

    _valider_username = field_validator("username")(UserCreate.valider_username.__func__)
    _valider_password = field_validator("password")(UserCreate.valider_password.__func__)


class UserMe(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_user: int
    name: str
    first_name: str
    username: str
    id_restaurant: int | None = None
    role: RoleRead 