from pydantic import BaseModel, ConfigDict

class PermissionsRead(BaseModel):
    # Grâce a sa Pydantic peut lire un objet de SQLAchemy et vérifier 
    model_config = ConfigDict(from_attributes=True)

    id_permission: int
    tag_permission: str

#POST    
class PermissionsCreate(BaseModel):
    
    tag_permission: str