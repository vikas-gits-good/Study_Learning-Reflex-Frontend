import reflex as rx
from ..gui import base_page
from ..navigation import Routes


@rx.page(route=Routes.HOME_PATH)
def home_page() -> rx.Component:
    my_child = rx.vstack(
        rx.heading("Home", size="6"),
        rx.text(
            "This is our home page",
            size="5",
        ),
        spacing="5",
        justify="start",
        align="center",
        min_height="85vh",
        id="my-child",
    )
    return base_page(child=my_child)
