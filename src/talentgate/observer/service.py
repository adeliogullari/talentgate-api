from typing import Any, Sequence
from sqlmodel import select, Session
from src.talentgate.observer.models import (
    Observer,
    CreateObserver,
    UpdateObserver,
    ObserverQueryParameters,
)


async def create(*, sqlmodel_session: Session, observer: CreateObserver) -> Observer:
    created_observer = Observer(
        **observer.model_dump(exclude_unset=True, exclude_none=True)
    )

    sqlmodel_session.add(created_observer)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_observer)

    return created_observer


async def retrieve_by_id(*, sqlmodel_session: Session, observer_id: int) -> Observer:
    statement: Any = select(Observer).where(Observer.id == observer_id)

    retrieved_observer = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_observer


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: ObserverQueryParameters
) -> Sequence[Observer]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = {
        getattr(Observer, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"}, exclude_unset=True, exclude_none=True
        )
    }

    statement: Any = select(Observer).offset(offset).limit(limit).where(*filters)

    retrieved_observer = sqlmodel_session.exec(statement).all()

    return retrieved_observer


async def update(
    *, sqlmodel_session: Session, retrieved_observer: Observer, observer: UpdateObserver
) -> Observer:
    retrieved_observer.sqlmodel_update(observer)

    sqlmodel_session.add(retrieved_observer)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_observer)

    return retrieved_observer


async def delete(
    *, sqlmodel_session: Session, retrieved_observer: Observer
) -> Observer:
    sqlmodel_session.delete(retrieved_observer)
    sqlmodel_session.commit()

    return retrieved_observer
