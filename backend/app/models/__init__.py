from app.models.base import Base, engine 
from app.models.restaurant import Restaurant
from app.models.product import Product
from app.models.user import User
from app.models.command import Command
from app.models.command_lines import Command_line 
from app.models.restaurant_address   import Restaurant_address
from app.models.permissions import Permission
from app.models.product_pictures import Product_picture
from app.models.role import Role

# Le schéma est géré par les migrations Alembic (dossier migrations/) :
# plus de create_all au démarrage.
