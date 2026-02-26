import reflex as rx

from Frontend import GUI

from .form import chat_form


def chat_page() -> rx.Component:
    return GUI.base_layout(
        rx.vstack(
            rx.heading(
                "Welcome to Reflex Chat!",
                chat_form(),
                size="9",
                id="chat-heading",
            ),
        )
    )
