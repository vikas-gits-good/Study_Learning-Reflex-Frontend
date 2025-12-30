import reflex as rx
from .navbar import _navbar
from .sidebar import _sidebar
from .footer import _footer


def base_page(
    child: rx.Component,
    navbar: bool = True,
    sidebar: bool = False,
    footer: bool = False,
    logo: bool = False,
    *args,
    **kwargs,
) -> rx.Component:
    return rx.fragment(
        _navbar() if navbar else None,
        _sidebar() if sidebar else None,
        rx.box(
            child,
            padding="1em",
            width="100%",
            id="base-child-container",
        ),
        _footer() if footer else None,
        rx.logo() if logo else None,
        rx.color_mode.button(position="bottom-right"),
        id="base-page-container",
    )
