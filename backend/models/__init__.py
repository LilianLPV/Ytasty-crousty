from models.base import Base, engine
from models.restaurant import Restaurant
from models.product import Product
from models.user import User
from models.command import Command
from models.command_lines import Command_line 
from models.restaurant_address   import Restaurant_address
from models.permissions import Permission
from models.product_pictures import Product_picture
from models.role import Role

Base.metadata.create_all(engine)