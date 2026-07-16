from pydantic import BaseModel, ConfigDict, Field
from app.schemas.command_lines import CommandLineRead
from datetime import datetime
from enum import Enum


# Valeur autorisée pour le statut
class StatusCommand(str, Enum):
    en_attente = "en attente"
    validee = "validée"
    en_preparation = "en préparation"
    prete = "prête"
    recuperee = "récupérée"
    annulee = "annulée"

# Valeur autorisée pour le retrait de la commande
class WithdrawalMethod(str, Enum):
    sur_place = "sur place"
    a_emporter = "à emporter"


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
    id_restaurant: int
    command_lines: list[CommandLineRead] = []

# La ligne que le client envoie
class CommandLineSend(BaseModel):
    id_product: int
    quantity: int = Field(ge=1)

#POST
class CommandCreate(BaseModel):
    
    withdrawal_method: WithdrawalMethod
    customer_information: str
    id_restaurant: int
    lines: list[CommandLineSend] = Field(min_length=1)


class CommandUpdateStatus(BaseModel):
    status_command: StatusCommand