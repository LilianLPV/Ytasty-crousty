from pydantic import BaseModel, ConfigDict
from app.schemas.restaurant_address import RestaurantAddressRead

#GET
class RestaurantRead(BaseModel):
    # Grâce a sa Pydantic peut lire un objet de SQLAchemy et vérifier 
    model_config = ConfigDict(from_attributes=True)

    id_restaurant: int
    name: str
    opening_status: bool
    opening_hours: str
    contact_details: str
    restaurant_address: RestaurantAddressRead


#POST
class RestaurantCreate(BaseModel):
    name: str
    opening_status: bool
    opening_hours: str
    contact_details: str
    id_address: int