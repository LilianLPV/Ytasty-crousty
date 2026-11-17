from pydantic import BaseModel, ConfigDict

class ProductPictureRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_picture: int
    picture: str
    id_product: int

class ProductPictureCreate(BaseModel):
    
    picture: str
    id_product: int      