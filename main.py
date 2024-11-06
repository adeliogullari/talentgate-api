from sqlmodel import SQLModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.talentgate.user.views import router as user_router
from src.talentgate.employee.views import router as employee_router
from src.talentgate.auth.views import router as auth_router
from src.talentgate.applicant.views import router as applicant_router
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
    {"name": "employee", "description": "Operations with employee"},
    {"name": "user", "description": "Operations with users"},
    {"name": "applicant", "description": "Operations with applicants"},
]

app.include_router(user_router)
app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(applicant_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
