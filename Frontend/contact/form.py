import reflex as rx
from .state import ContactState


def contact_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.hstack(
                rx.input(
                    placeholder="First Name",
                    name="first_name",
                    required=True,
                    type="text",
                    width="100%",
                ),
                rx.input(
                    placeholder="Last Name",
                    name="last_name",
                    type="text",
                    width="100%",
                ),
                width="100%",
            ),
            rx.input(
                placeholder="first.last@domain.com",
                name="user_email",
                type="email",
                required=True,
                width="100%",
            ),
            rx.text_area(
                placeholder="Your message goes here.",
                name="user_message",
                required=True,
                width="100%",
            ),
            rx.checkbox(
                text="Accept T&C",
                name="cb_tnc",
                required=True,
                default_checked=True,
            ),
            rx.checkbox(
                text="Subscribe to Newsletter",
                name="cb_subsc_nwsltr",
                required=False,
                default_checked=False,
            ),
            rx.button(
                "Submit",
                name="cb_submit",
            ),
            justify="start",
            align="start",
        ),
        on_submit=ContactState.handle_submit,
        reset_on_submit=True,
    )
