import reflex as rx
from ..gui import base_page
from ..navigation import Routes


@rx.page(route=Routes.ABOUT_PATH)
def about_page() -> rx.Component:
    my_child = rx.vstack(
        rx.heading("About us", size="6"),
        rx.text(
            "Something cool about us",
        ),
        spacing="5",
        justify="start",
        align="center",
        min_height="85vh",
        id="my-child",
    )
    return base_page(child=my_child)
