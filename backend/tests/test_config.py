from app.config import get_cors_origins, get_database_url


def test_url_scalingo_convertie_pour_psycopg(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@host:5432/db?sslmode=prefer")
    assert get_database_url() == "postgresql+psycopg://user:pass@host:5432/db?sslmode=prefer"


def test_url_deja_au_bon_format(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://admin:pw@localhost:5432/ytasty_db")
    assert get_database_url() == "postgresql+psycopg://admin:pw@localhost:5432/ytasty_db"


def test_origines_cors(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "https://client.osc-fr1.scalingo.io/, http://localhost:5173")
    assert get_cors_origins() == ["https://client.osc-fr1.scalingo.io", "http://localhost:5173"]
