from pydantic import BaseModel, ConfigDict

class ProductRead(BaseModel):
    # Grâce a sa Pydantic peut lire un objet de SQLAchemy et vérifier 
    model_config = ConfigDict(from_attributes=True)

    id_product: int
    name: str
    description: str
    price: float
    availability: bool
    category: str
    ingredient_list: str

#POST 
class ProductCreate(BaseModel):
    
    name: str
    description: str
    price: float
    availability: bool
    category: str
    ingredient_list: str
    id_restaurant: int
