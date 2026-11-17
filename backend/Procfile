web: uvicorn main:app --host 0.0.0.0 --port $PORT
postdeploy: alembic upgrade head
