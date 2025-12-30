import reflex as rx
from ..gui import base_page
from ..navigation import Routes
from ..contact import ContactState, contact_form


@rx.page(route=Routes.CONTACT_PATH)
def contact_page() -> rx.Component:
    my_child = rx.vstack(
        rx.heading("Contact us", size="6"),
        rx.vstack(
            rx.cond(
                ContactState.form_submit,
                ContactState.thanks,
                "Please enter the form and submit.",
            ),
            rx.desktop_only(
                rx.box(
                    contact_form(),
                    width="50vw",
                )
            ),
            rx.mobile_and_tablet(
                rx.box(
                    contact_form(),
                    width="85vw",
                )
            ),
            align="start",
        ),
        spacing="5",
        justify="start",
        align="center",
        min_height="85vh",
        id="my-child",
    )
    return base_page(child=my_child)
