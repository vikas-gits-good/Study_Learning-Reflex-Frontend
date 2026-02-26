import reflex as rx

from Frontend import GUI
from rxconfig import config


def about() -> rx.Component:
    # About Page (about)
    return GUI.base_layout(
        rx.vstack(
            rx.heading(
                "Welcome to Reflex about!",
                size="9",
                id="about-heading",
            ),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
                id="about-text",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )
