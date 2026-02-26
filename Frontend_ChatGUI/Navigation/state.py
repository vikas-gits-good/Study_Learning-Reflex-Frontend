import reflex as rx

from .routes import Routes


class NavState(rx.State):
    @staticmethod
    def to_home() -> rx.event.EventSpec:
        return rx.redirect(Routes.HOME)

    @staticmethod
    def to_about() -> rx.event.EventSpec:
        return rx.redirect(Routes.ABOUT)

    @staticmethod
    def to_chat() -> rx.event.EventSpec:
        return rx.redirect(Routes.CHAT)
