# Ytasty Crousty

Application de commande pour les restaurants Ytasty Crousty (Aix, Lyon, Paris) :
un client web React, une API FastAPI et une base PostgreSQL, déployés sur Scalingo.

- Client : `https://<url-du-client>` <!-- à compléter après le déploiement -->
- API : `https://<url-de-l-api>` (documentation sur `/docs`, santé sur `/health`)

## Architecture

```
Navigateur ──HTTPS──▶ App client (frontend/)      React + TypeScript, build Vite servi par `serve`
     │
     └──HTTPS (fetch JSON)──▶ App API (backend/)  FastAPI + SQLAlchemy, uvicorn sur $PORT
                                   │
                                   └──SQL──▶ Addon PostgreSQL Starter 512
```

Le dépôt est un monorepo : chaque app Scalingo pointe vers son dossier grâce à `PROJECT_DIR`.
Le schéma de la base est géré par Alembic (`backend/migrations/`) ; les migrations sont jouées
automatiquement après chaque déploiement (process `postdeploy` du `Procfile`).

## Lancer le projet en local

Prérequis : Python 3.11+, Node.js 22, Docker Desktop.

```bash
# 1. Variables d'environnement
cp .env.example .env                    # puis remplir les valeurs
cp frontend/.env.example frontend/.env  # VITE_API_URL vide en local

# 2. Base PostgreSQL
docker compose up -d db

# 3. API
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements-dev.txt
alembic upgrade head          # crée les tables
python create_script.py       # données initiales (relançable sans doublons)
uvicorn main:app --reload     # http://127.0.0.1:8000/docs

# 4. Client (autre terminal)
cd frontend
npm install
npm run dev                   # http://localhost:5173 (proxy /api → API locale)
```

> Base créée avant Alembic (avec l'ancien `create_all`) ? Marquez-la comme à jour une fois :
> `alembic stamp head`.

Tests de l'API (base locale migrée et peuplée) : `cd backend && pytest`.

## Déploiement sur Scalingo

### App API

```bash
scalingo create ytasty-api --region osc-fr1
scalingo --app ytasty-api env-set PROJECT_DIR=backend
scalingo --app ytasty-api addons-add postgresql postgresql-starter-512
scalingo --app ytasty-api env-set SECRET_KEY=<clé longue et aléatoire> \
  ADMIN_USERNAME=<admin> ADMIN_PASSWORD=<mot de passe> \
  CORS_ORIGINS=https://<url-du-client>
git push scalingo main        # ou Auto Deploy depuis GitHub
scalingo --app ytasty-api run python create_script.py   # une seule fois
```

L'addon fournit `SCALINGO_POSTGRESQL_URL` et son alias `DATABASE_URL` ;
`app/config.py` les convertit au format `postgresql+psycopg://` attendu par SQLAlchemy.

### App client

```bash
scalingo create ytasty-client --region osc-fr1
scalingo --app ytasty-client env-set PROJECT_DIR=frontend VITE_API_URL=https://<url-de-l-api>
git push scalingo main
```

Scalingo lance `npm run build` puis `npm start` (`serve -s dist`, qui renvoie `index.html`
pour les routes internes). `VITE_API_URL` est figée au build : la modifier impose un redéploiement.

### Déploiement continu

Chaque app est liée au dépôt GitHub avec *Auto Deploy* sur `main`. Les GitHub Actions
(`.github/workflows/`) lancent lint, build et tests uniquement sur le dossier modifié ;
Scalingo attend qu'elles soient vertes avant de déployer.

## Variables d'environnement

| App | Variable | Rôle |
|---|---|---|
| API | `DATABASE_URL` / `SCALINGO_POSTGRESQL_URL` | URL de la base (fournie par l'addon sur Scalingo) |
| API | `SECRET_KEY` | Signature des tokens JWT |
| API | `CORS_ORIGINS` | Origines autorisées, séparées par des virgules |
| API | `ADMIN_USERNAME`, `ADMIN_PASSWORD` | Compte admin créé par `create_script.py` |
| API | `PROJECT_DIR` | `backend` |
| Client | `VITE_API_URL` | URL publique de l'API, figée au build |
| Client | `PROJECT_DIR` | `frontend` |
| Local | `POSTGRES_PASSWORD` | Mot de passe du conteneur PostgreSQL |

Aucune valeur secrète n'est commitée : voir `.env.example` et `frontend/.env.example`.

## Coûts

| Ressource | Taille | Estimation / mois | Réel / mois |
|---|---|---|---|
| App API | 1 conteneur S | à compléter (simulateur Scalingo) | à compléter |
| App client | 1 conteneur S | à compléter | à compléter |
| PostgreSQL | Starter 512 | à compléter | à compléter |

## En cas de panne

<!-- À compléter avec les commandes réellement testées (étape 05) -->

- Logs : `scalingo --app ytasty-api logs --lines 200`
- Rollback : …
- Sauvegarde et restauration de la base : …
