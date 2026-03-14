from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.resume.models import ParsedResume

router = APIRouter(tags=["resume"])


@router.post(
    path="/api/v1/resume/parse",
    response_model=ParsedResume,
    status_code=201,
)
async def parse_resume(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> None:
    pass
