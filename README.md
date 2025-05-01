# talentgate-api
TalentGate Restful Service

### Development

```commandline
fastapi dev main.py
```

#### Docker
```commandline
docker-compose up --build
```

### Production

```commandline
fastapi run main.py
```

#### Docker
```commandline
docker-compose up --build --scale app=5
```
