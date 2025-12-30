import asyncio
import reflex as rx

from .model import ContactModel


class ContactState(rx.State):
    form_data: dict = {}
    form_submit: bool = False
    time_left: int = 5

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
