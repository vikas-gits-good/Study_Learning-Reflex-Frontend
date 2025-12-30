import asyncio
import reflex as rx

from typing import Sequence
from sqlmodel import select
from .model import ContactModel


class ContactState(rx.State):
    form_data: dict = {}
    entries: Sequence[ContactModel] = []
    form_submit: bool = False

    @rx.var
    def thanks(self) -> str:
        first_name: str = self.form_data.get("first_name", "")
        return f"Thank you for reaching out {first_name}".strip() + "!"

    async def handle_submit(self, form_data: dict):
        self.form_data = form_data
        data = {}
        for key, val in form_data.items():
            if val == "" or val is None:
                continue
            data[key] = val

        # add user contact form data to database
        with rx.session() as sesn:
            db_entry = ContactModel(**data)
            sesn.add(db_entry)
            sesn.commit()
            self.form_submit = True
            yield

        # reset after form submission
        await asyncio.sleep(2)
        self.form_submit = False
        yield

    def list_entries(self):
        with rx.session() as sesn:
            entries = sesn.exec(
                select(ContactModel),
            ).all()
            self.entries = entries
