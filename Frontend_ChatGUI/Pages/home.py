import reflex as rx

from Frontend_ChatGUI import GUI
from rxconfig import config


def home() -> rx.Component:
    # Welcome Page (home)
    return GUI.base_layout(
        rx.vstack(
            rx.heading(
                "Welcome to Reflex GPT!",
                size="9",
                id="home-heading",
            ),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
                id="home-text",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
                id="home-link",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )
