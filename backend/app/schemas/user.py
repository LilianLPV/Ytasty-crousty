from pydantic import BaseModel, ConfigDict

class UserRead(BaseModel):
    # Grâce a sa Pydantic peut lire un objet de SQLAchemy et vérifier 
    model_config = ConfigDict(from_attributes=True)

    id_user: int
    name: str
    first_name: str
    username: str

#POST
class UserCreate(BaseModel):
    
    name: str
    first_name: str
    username: str
    password: str
    id_role: int