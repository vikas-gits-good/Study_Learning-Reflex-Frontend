import reflex as rx
from .model import ContactModel


def render_contact_list(contact: ContactModel):
    return rx.box(
        rx.heading(contact.first_name, align="center"),
        rx.text(contact.user_message),
    )
