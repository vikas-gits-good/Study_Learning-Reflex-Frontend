import reflex as rx
from ..navigation import Routes, NavState


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(rx.text(text, size="4", weight="medium"), href=url)


def _navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.link(
                        rx.image(
                            src="./logo.jpg",
                            width="2em",
                            height="auto",
                            border_radius="25%",
                        ),
                        href=Routes.HOME_PATH,
                        is_external=False,
                    ),
                    rx.link(
                        rx.heading("Reflex", size="7", weight="bold"),
                        href=Routes.HOME_PATH,
                        underline="none",
                        is_external=False,
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Home", Routes.HOME_PATH),
                    navbar_link("About", Routes.ABOUT_PATH),
                    navbar_link("Pricing", Routes.PRICING_PATH),
                    navbar_link("Contact", Routes.CONTACT_PATH),
                    spacing="5",
                ),
                rx.hstack(
                    rx.button(
                        "Sign Up",
                        size="3",
                        variant="outline",
                        on_click=NavState.to_signup,
                    ),
                    rx.button(
                        "Log In",
                        size="3",
                        on_click=NavState.to_login,
                    ),
                    spacing="4",
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.link(
                        rx.image(
                            src="./logo.jpg",
                            width="2em",
                            height="auto",
                            border_radius="25%",
                        ),
                        href=Routes.HOME_PATH,
                        is_external=False,
                    ),
                    rx.link(
                        rx.heading("Reflex", size="7", weight="bold"),
                        href=Routes.HOME_PATH,
                        underline="none",
                        is_external=False,
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        rx.menu.item("Home", on_click=NavState.to_home),
                        rx.menu.item("About", on_click=NavState.to_about),
                        rx.menu.item("Pricing", on_click=NavState.to_pricing),
                        rx.menu.item("Contact", on_click=NavState.to_contact),
                        rx.menu.separator(),
                        rx.menu.item("Sign up", on_click=NavState.to_signup),
                        rx.menu.item("Log in", on_click=NavState.to_login),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        width="100%",
    )
