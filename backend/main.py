from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Restaurant, Restaurant_address, User,Role,Permission,Command,Command_line,Product,engine


# ---------- CREATE ----------
print("=== CREATE ===")
with Session(engine) as session:
    # L'adresse et le restaurant (relation localise)
    adresse = Restaurant_address(city="Aix-en-Provence", address="12 cours Mirabeau")
    resto = Restaurant(
        name="Ytasty Crousty Aix",
        opening_status=True,
        opening_hours="11h-23h",
        contact_details="04 42 00 00 00",
        restaurant_address=adresse,
    )

    # Le rôle, ses permissions (relation inclut, many-to-many) et un user (relation attribue)
    role_admin = Role(role_name="administrateur")
    perm_delete = Permission(tag_permission="delete_product")
    perm_update = Permission(tag_permission="update_product")
    role_admin.permissions.append(perm_delete)
    role_admin.permissions.append(perm_update)

    user = User(
        name="Dupont",
        first_name="Marie",
        username="mdupont2026",
        password="MotDePasse123!",
        role=role_admin,
    )

    # Un produit vendu par le resto (relation vend)
    produit = Product(
        name="Crousty Burger",
        description="Le burger signature",
        price=8.50,
        availability=True,
        category="burgers",
        ingredient_list="pain, steak, cheddar, salade, sauce crousty",
        restaurant=resto,
    )

    # Une commande reçue par le resto (relation recoit)...
    commande = Command(
        number_command="CMD-0001",
        creation_date_and_time=datetime.now(),
        status_command="en attente",
        withdrawal_method="sur place",
        customer_information="Jean Martin - 06 12 34 56 78",
        price_total=17.00,
    )
    commande.restaurant = resto

    # ...avec une ligne : 2 Crousty Burgers (relations contient + concerne)
    ligne = Command_line(
        quantity=2,
        unit_price=8.50,
        command=commande,
        product=produit,
    )

    session.add_all([user, produit, commande, ligne])
    session.commit()
    print("Tout est créé : resto + adresse, user + rôle + permissions, produit, commande + ligne")

# ---------- READ ----------
print("\n=== READ ===")
with Session(engine) as session:
    # Les relations en action : chaque ligne traverse plusieurs tables sans requête manuelle
    resto = session.get(Restaurant, 1)
    print(f"{resto.name} - {resto.restaurant_address.city}, {resto.restaurant_address.address}")
    print(f"Produits : {[p.name for p in resto.products]}")
    print(f"Commandes reçues : {[c.number_command for c in resto.commands]}")

    user = session.scalars(select(User)).first()
    print(f"{user.first_name} {user.name} est {user.role.role_name}")
    print(f"Ses permissions : {[p.tag_permission for p in user.role.permissions]}")

    cmd = session.get(Command, 1)
    print(f"Détail de {cmd.number_command} :")
    for l in cmd.command_lines:
        print(f"  {l.quantity} x {l.product.name} à {l.unit_price}€ = {l.quantity * l.unit_price}€")

# ---------- UPDATE ----------
print("\n=== UPDATE ===")
with Session(engine) as session:
    commande = session.scalars(
        select(Command).where(Command.number_command == "CMD-0001")
    ).first()
    if commande:
        commande.status_command = "en préparation"
        session.commit()
        print(f"{commande.number_command} passe au statut : {commande.status_command}")

# ---------- DELETE ----------
print("\n=== DELETE ===")
with Session(engine) as session:
    user = session.scalars(
        select(User).where(User.username == "mdupont2026")
    ).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"Utilisateur {user.username} supprimé")

    nb_users = len(session.scalars(select(User)).all())
    print(f"Utilisateurs restants : {nb_users}")