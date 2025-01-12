from sqlmodel import SQLModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.talentgate.user.views import router as user_router
from src.talentgate.subscription.views import router as subscription_router
from src.talentgate.employee.views import router as employee_router
from src.talentgate.auth.views import router as auth_router
from src.talentgate.location.views import router as location_router
from src.talentgate.application.views import router as application_router
from src.talentgate.job.views import router as job_router
from src.talentgate.company.views import router as company_router
from src.talentgate.database.service import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.version = "0.1.0"
app.title = "TalentGate"
app.description = "TalentGate Platform"

app.openapi_tags = [
    {"name": "auth", "description": "Operations with auth"},
    {"name": "location", "description": "Operations with location"},
    {"name": "employee", "description": "Operations with employee"},
    {"name": "user", "description": "Operations with users"},
    {"name": "subscription", "description": "Operations with subscriptions"},
    {"name": "application", "description": "Operations with applications"},
    {"name": "job", "description": "Operations with jobs"},
    {"name": "company", "description": "Operations with companies"},
]

app.include_router(user_router)
app.include_router(subscription_router)
app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(location_router)
app.include_router(application_router)
app.include_router(job_router)
app.include_router(company_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
