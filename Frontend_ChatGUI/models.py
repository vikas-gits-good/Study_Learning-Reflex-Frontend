import os
from datetime import datetime, timedelta, timezone

import reflex as rx
import sqlalchemy as sa
from dotenv import load_dotenv
from sqlmodel import Field

load_dotenv(".env")


def get_tz_now() -> datetime:
    hrs, min = os.getenv("TIMEZONE", "05:30").split(":")
    tz = timezone(timedelta(hours=int(hrs), minutes=int(min)))
    return datetime.now(tz)


class ChatModel(rx.Model, table=True):
    # ids: str
    # messages: list[str]
    title: str
    created_at: datetime = Field(
        default_factory=get_tz_now,
        sa_type=sa.DateTime(timezone=True),  # type:ignore
        sa_column_kwargs={
            "server_default": sa.func.now(),
        },
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=get_tz_now,
        sa_type=sa.DateTime(timezone=True),  # type:ignore
        sa_column_kwargs={
            "onupdate": sa.func.now(),
            "server_default": sa.func.now(),
        },
        nullable=False,
    )


# class ChatMessageModel(rx.Model, table=True):
#     pass
