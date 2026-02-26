"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from . import Pages

app = rx.App()
app.add_page(Pages.home, route="/")
app.add_page(Pages.about, route="/about")
