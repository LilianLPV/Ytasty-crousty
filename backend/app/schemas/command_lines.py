from pydantic import BaseModel, ConfigDict

class CommandLineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_command_line: int
    quantity: int
    unit_price: float
    id_command: int
    id_product: int

class CommandLineCreate(BaseModel):
    quantity: int
    id_command: int
    id_product: int