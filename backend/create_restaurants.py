from app.models.base import engine
from app.models.restaurant import Restaurant
from app.models.restaurant_address import Restaurant_address
from sqlalchemy.orm import Session
from sqlalchemy import select

# Les 3 restaurants à créer (nom, ville, adresse)
restaurants_data = [
    {"name": "Ytasty Crousty Aix", "city": "Aix-en-Provence", "contact_details": "06 07 08 09 10" ,"address": "500 Rte de Berre, 13090"},
    {"name": "Ytasty Crousty Lyon", "city": "Lyon", "contact_details": "07 11 12 13 14", "address": "92 Bd des États-Unis, 69008"},
    {"name": "Ytasty Crousty Paris", "city": "Paris", "contact_details": "07 15 16 17 18", "address": "Paris 19, 178 Av. Jean Jaurès, 75019"},
]

with Session(engine) as session:
    for data in restaurants_data:
        # 1. Vérifier si le restaurant existe déjà (par son nom)
        existe = session.scalars(
            select(Restaurant).where(Restaurant.name == data["name"])
        ).first()

        if existe is None:
            # 2. Créer l'adresse
            adresse = Restaurant_address(city=data["city"], address=data["address"])
            # 3. Créer le restaurant lié à l'adresse
            resto = Restaurant(
                name=data["name"],
                opening_status=True,
                opening_hours="11h-23h",
                contact_details=data["contact_details"],
                restaurant_address=adresse,  
            )
            session.add(resto)
            print(f"Restaurant créé : {data['name']}")
        else:
            print(f"{data['name']} existe déjà")

    session.commit()