from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from src.talentgate.application.views import router as application_router
from src.talentgate.auth.views import router as auth_router
from src.talentgate.company.views import router as company_router
from src.talentgate.database.service import get_sqlmodel_engine
from src.talentgate.job.views import router as job_router
from src.talentgate.payment.views import router as payment_router
from src.talentgate.user.views import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    engine = get_sqlmodel_engine()
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.version = "0.1.0"
app.title = "TalentGate"
app.description = "TalentGate Platform"

app.openapi_tags = [
    {"name": "auth", "description": "Operations with auth"},
    {"name": "users", "description": "Operations with users"},
    {"name": "companies", "description": "Operations with companies"},
    {"name": "location", "description": "Operations with location"},
    {"name": "application", "description": "Operations with applications"},
    {"name": "job", "description": "Operations with jobs"},
    {"name": "payment", "description": "Operations with payments"},
]

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(company_router)
app.include_router(application_router)
app.include_router(job_router)
app.include_router(payment_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
