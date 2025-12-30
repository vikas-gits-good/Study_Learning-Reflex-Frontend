import reflex as rx

import sqlalchemy
from sqlmodel import Field
from datetime import datetime, timezone


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ContactModel(rx.Model, table=True):
    first_name: str
    last_name: str | None = None
    user_email: str
    user_message: str
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False,
    )
