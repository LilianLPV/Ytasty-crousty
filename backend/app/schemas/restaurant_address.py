from pydantic import BaseModel, ConfigDict

class RestaurantAddressRead(BaseModel):
    # Grâce a sa Pydantic peut lire un objet de SQLAchemy et vérifier 
    model_config = ConfigDict(from_attributes=True)

    id_address: int
    city: str
    address: str


class RestaurantAddressCreate(BaseModel):
    city: str
    address: str