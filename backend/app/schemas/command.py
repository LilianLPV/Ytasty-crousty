from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CommandRead(BaseModel):
    # Grâce a sa Pydantic peut lire un objet de SQLAchemy et vérifier 
    model_config = ConfigDict(from_attributes=True)

    id_command: int
    number_command: str
    creation_date_and_time: datetime
    status_command: str
    withdrawal_method: str
    customer_information: str
    price_total: float

class CommandCreate(BaseModel):
    
    number_command: str
    creation_date_and_time: datetime
    status_command: str
    withdrawal_method: str
    customer_information: str
    price_total: float
    id_restaurant: int