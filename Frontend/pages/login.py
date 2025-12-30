import reflex as rx
from ..gui import base_page
from ..navigation import Routes


@rx.page(route=Routes.LOGIN_PATH)
def login_page() -> rx.Component:
    my_child = rx.vstack(
        rx.heading("Login", size="6"),
        rx.text("This is our login"),
        spacing="5",
        justify="start",
        align="center",
        min_height="85vh",
        id="my-child",
    )
    return base_page(child=my_child)
