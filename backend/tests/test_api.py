"""Tests de fumée de l'API.

Ils ont besoin d'une base PostgreSQL migrée (alembic upgrade head) et peuplée
(python create_script.py) : en CI, c'est fait par le workflow GitHub Actions.
"""
import os

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ytasty Crousty API"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_liste_des_restaurants():
    response = client.get("/restaurants/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_login_refuse_un_mauvais_mot_de_passe():
    response = client.post("/auth/login", data={"username": "admin", "password": "faux"})
    assert response.status_code == 401


def test_login_puis_me():
    response = client.post(
        "/auth/login",
        data={
            "username": os.getenv("ADMIN_USERNAME", "admin"),
            "password": os.getenv("ADMIN_PASSWORD", "Admin1234!"),
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == os.getenv("ADMIN_USERNAME", "admin")
