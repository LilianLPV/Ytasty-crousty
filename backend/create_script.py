import os
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.base import engine
from app.models.role import Role
from app.models.permissions import Permission
from app.models.restaurant import Restaurant
from app.models.restaurant_address import Restaurant_address
from app.models.user import User
from app.models.product import Product
from app.models.product_pictures import Product_picture
from app.models.command import Command
from app.models.command_lines import Command_line
from app.utils.jwt import hash_password

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin1234!")


def get_or_create(session, model, defaults=None, **filtres):
    """Retourne l'objet existant correspondant aux filtres, ou le crée."""
    instance = session.scalars(
        select(model).filter_by(**filtres)
    ).first()
    if instance is not None:
        return instance, False
    params = {**filtres, **(defaults or {})}
    instance = model(**params)
    session.add(instance)
    session.flush()  
    return instance, True


with Session(engine) as session:
    # RÔLES
    role_admin, _ = get_or_create(session, Role, role_name="administrateur")
    role_perso, _ = get_or_create(session, Role, role_name="personnel")
    role_direction, _ = get_or_create(session, Role, role_name="direction")
    print("Rôles OK")

    # PERMISSION
    perm_names = [
        "create_product", "update_product", "delete_product",
        "manage_users", "manage_commands", "view_stats",
    ]
    permissions = {}
    for tag in perm_names:
        perm, _ = get_or_create(session, Permission, tag_permission=tag)
        permissions[tag] = perm

    role_admin.permissions = list(permissions.values())
    print("Permissions OK")

    # ADRESSE + RESTAURANT
    restaurants_data = [
        {"name": "Ytasty Crousty Aix", "city": "Aix-en-Provence",
         "address": "500 Rte de Berre, 13090", "contact": "06 07 08 09 10"},
        {"name": "Ytasty Crousty Lyon", "city": "Lyon",
         "address": "92 Bd des États-Unis, 69008", "contact": "07 11 12 13 14"},
        {"name": "Ytasty Crousty Paris", "city": "Paris",
         "address": "178 Av. Jean Jaurès, 75019", "contact": "07 15 16 17 18"},
    ]
    restaurants = {}
    for data in restaurants_data:
        resto = session.scalars(
            select(Restaurant).where(Restaurant.name == data["name"])
        ).first()
        if resto is None:
            adresse = Restaurant_address(city=data["city"], address=data["address"])
            resto = Restaurant(
                name=data["name"],
                opening_status=True,
                opening_hours="11h-23h",
                contact_details=data["contact"],
                restaurant_address=adresse,
            )
            session.add(resto)
            session.flush()
        restaurants[data["city"]] = resto
    print("Restaurants OK")

    # UTILISATEUR
 
    admin = session.scalars(
        select(User).where(User.username == ADMIN_USERNAME)
    ).first()
    if admin is None:
        admin = User(
            name="Admin", first_name="Super",
            username=ADMIN_USERNAME,
            password=hash_password(ADMIN_PASSWORD),
            id_role=role_admin.id_role,
        )
        session.add(admin)
    
    perso_aix = session.scalars(
        select(User).where(User.username == "perso_aix")
    ).first()
    if perso_aix is None:
        perso_aix = User(
            name="Martin", first_name="Julie",
            username="perso_aix",
            password=hash_password("Personnel123!"),
            id_role=role_perso.id_role,
            id_restaurant=restaurants["Aix-en-Provence"].id_restaurant,
        )
        session.add(perso_aix)
    print("Users OK")

    # PRODUITS
    carte = [
        # BURGERS
        {"name": "Crousty Burger", "description": "Le burger signature au poulet pané et cheddar",
         "price": 8.50, "category": "burgers",
         "ingredient_list": "pain, poulet pané, cheddar, salade, tomate, sauce crousty"},
        {"name": "Double Crousty", "description": "Double poulet pané, double cheddar",
         "price": 11.50, "category": "burgers",
         "ingredient_list": "pain, 2 poulets pané, 2 cheddar, oignons, sauce crousty"},
        {"name": "Triple Crousty", "description": "Triple poulet pané croustillant",
         "price": 13.00, "category": "burgers",
         "ingredient_list": "pain, poulet pané, salade, mayonnaise"},
        {"name": "Veggie Crousty", "description": "Burger végétarien galette de légumes",
         "price": 8.00, "category": "burgers",
         "ingredient_list": "pain, galette légumes, salade, tomate, sauce"},

        # ACCOMPAGNEMENTS
        {"name": "Frites Maison", "description": "Frites fraîches coupées main",
         "price": 3.50, "category": "accompagnements",
         "ingredient_list": "pommes de terre, sel"},
        {"name": "Potatoes", "description": "Pommes de terre épicées",
         "price": 4.00, "category": "accompagnements",
         "ingredient_list": "pommes de terre, épices"},
        {"name": "Onion Rings", "description": "Rondelles d'oignon panées",
         "price": 4.50, "category": "accompagnements",
         "ingredient_list": "oignons, panure"},
        {"name": "Nuggets x6", "description": "6 nuggets de poulet",
         "price": 5.00, "category": "accompagnements",
         "ingredient_list": "poulet pané"},

        # BOISSONS
        {"name": "Coca-Cola", "description": "Canette 33cl",
         "price": 2.50, "category": "boissons",
         "ingredient_list": "soda"},
        {"name": "Eau minérale", "description": "Bouteille 50cl",
         "price": 2.00, "category": "boissons",
         "ingredient_list": "eau"},
        {"name": "Jus d'orange", "description": "Jus pressé 33cl",
         "price": 3.00, "category": "boissons",
         "ingredient_list": "orange"},

        # DESSERTS
        {"name": "Sundae Chocolat", "description": "Glace vanille sauce chocolat",
         "price": 3.00, "category": "desserts",
         "ingredient_list": "glace, chocolat"},
        {"name": "Cookie", "description": "Cookie tout chocolat",
         "price": 2.00, "category": "desserts",
         "ingredient_list": "farine, pépites chocolat, beurre"},
        {"name": "Muffin Myrtille", "description": "Muffin moelleux aux myrtilles",
         "price": 2.50, "category": "desserts",
         "ingredient_list": "farine, myrtilles, sucre"},

        # MENUS
        {"name": "Menu Crousty", "description": "Crousty Burger + frites + boisson",
         "price": 12.90, "category": "menus",
         "ingredient_list": "Crousty Burger, frites, boisson au choix"},
        {"name": "Menu Enfant", "description": "Cheeseburger + nuggets + jus + jouet",
         "price": 7.90, "category": "menus",
         "ingredient_list": "cheeseburger, nuggets, jus, jouet"},
    ]
    produits = {}  # clé = (nom, ville) -> produit
    for ville, resto in restaurants.items():
        for item in carte:
            prod = session.scalars(
                select(Product).where(
                    Product.name == item["name"],
                    Product.id_restaurant == resto.id_restaurant,
                )
            ).first()
            if prod is None:
                prod = Product(
                    name=item["name"],
                    description=item["description"],
                    price=item["price"],
                    availability=True,
                    category=item["category"],
                    ingredient_list=item["ingredient_list"],
                    id_restaurant=resto.id_restaurant,
                )
                session.add(prod)
                session.flush()
            produits[(item["name"], ville)] = prod
    print(f"Produits OK ({len(carte)} x {len(restaurants)} restaurants)")
    for nom_prod, fichier in [("Crousty Burger", "crousty_burger.png"),
                              ("Double Crousty", "double_crousty.png"),
                              ("Triple Crousty", "triple_crousty.png"),
                              ("Veggie Crousty", "veggie_crousty.jpg"),
                              ("Frites Maison", "frite.png"),
                              ("Potatoes", "potatoes.png"),
                              ("Onion Rings", "onion_ring.jpg"),
                              ("Nuggets x6", "nugget.png"),
                              ("Coca-Cola", "coca_cola.png"),
                              ("Eau minérale", "eau.png"),
                              ("Jus d'orange", "jus_orange.png"),
                              ("Sundae Chocolat", "sundae_chocolate.png"),
                              ("Cookie", "cookie.png"),
                              ("Muffin Myrtille", "muffin_myrtille.png"),
                              ("Menu Crousty", "menu_crousty.png"),
                              ("Menu Enfant", "menu_enfant.png")]:
        for ville in restaurants:
            prod = produits[nom_prod, ville]
            existe = session.scalars(
                select(Product_picture).where(Product_picture.id_product == prod.id_product)
            ).first()
            if existe is None:
                session.add(Product_picture(picture=fichier, id_product=prod.id_product))
            else:
                existe.picture = fichier
    print("Images OK")
    # COMMANDES
    cmd = session.scalars(
        select(Command).where(Command.number_command == "CMD-0001")
    ).first()
    if cmd is None:
        cmd = Command(
            number_command="CMD-0001",
            creation_date_and_time=datetime.now(),
            status_command="en attente",
            withdrawal_method="sur place",
            customer_information="Jean Client - 06 00 00 00 00",
            price_total=20.50,
            id_restaurant=restaurants["Aix-en-Provence"].id_restaurant,
        )
        session.add(cmd)
        session.flush()

        session.add(Command_line(
            quantity=2, unit_price=8.50,
            id_command=cmd.id_command,
            id_product=produits["Crousty Burger", "Aix-en-Provence"].id_product,
        ))
        session.add(Command_line(
            quantity=1, unit_price=3.50,
            id_command=cmd.id_command,
            id_product=produits["Frites Maison", "Aix-en-Provence"].id_product,
        ))
    print("Commande OK")

    session.commit()
    print("\n Base peuplée avec succès !")
    print(f"   Admin : {ADMIN_USERNAME} / (mot de passe du .env)")
    print(f"   Personnel Aix : perso_aix / Personnel123!")