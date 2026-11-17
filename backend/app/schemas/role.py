from pydantic import BaseModel, ConfigDict

class RoleRead(BaseModel):
    # Grâce a sa Pydantic peut lire un objet de SQLAchemy et vérifier 
    model_config = ConfigDict(from_attributes=True)

    id_role: int
    role_name: str

#POST    
class RoleCreate(BaseModel):
    
    role_name: str
