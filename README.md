# talentgate-api
TalentGate Restful Service

### Development

```commandline
docker compose up --build
fastapi dev main.py
alembic revision --autogenerate -m "migration"
alembic upgrade head
```

### Production

```commandline
docker compose up --build --scale app=5
fastapi run main.py
docker compose run --rm talentgate-api alembic upgrade head
```

##### Postgres

_Backup_
```commandline
ssh user@vps \
  "PGPASSWORD='${POSTGRES_PASSWORD}' \
   docker exec postgres \
   pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} | gzip" \
  > postgres_$(date +%F).sql.gz
```

_Restore_
```commandline
gunzip -c postgres_2025-01-10.sql.gz | \
ssh user@vps \
  "docker exec -i postgres psql -U admin talentgate"
```


##### Minio

_Backup_
```commandline
ssh user@vps \
  "docker exec minio \
   tar -C /data -czf -" \
> minio_$(date +%F).tar.gz
```

_Restore_
```commandline
gunzip -c minio_2025-01-10.tar.gz | \
ssh user@vps \
  "docker exec -i minio \
   tar -C /data -xzf -"
```
