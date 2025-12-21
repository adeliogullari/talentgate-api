# talentgate-api
TalentGate Restful Service

### Development

```commandline
docker-compose up --build
fastapi dev main.py
alembic revision --autogenerate -m "migration"
alembic upgrade head
```

### Production

```commandline
docker-compose up --build --scale app=5
fastapi run main.py
```