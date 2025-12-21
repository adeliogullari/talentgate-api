from sqlmodel import SQLModel


class BaseModel(SQLModel):
    model_config = {
        "extra": "ignore",
        "from_attributes": True,
    }
