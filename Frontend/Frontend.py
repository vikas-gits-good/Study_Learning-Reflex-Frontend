"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from . import Navigation, Pages

app = rx.App()
app.add_page(Pages.home, route=Navigation.Routes.HOME)
app.add_page(Pages.about, route=Navigation.Routes.ABOUT)
