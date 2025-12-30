import reflex as rx

from .routes import Routes


class NavState(rx.State):
    def to_home(self):
        return rx.redirect(path=Routes.HOME_PATH)

    def to_about(self):
        return rx.redirect(path=Routes.ABOUT_PATH)

    def to_pricing(self):
        return rx.redirect(path=Routes.PRICING_PATH)

    def to_contact(self):
        return rx.redirect(path=Routes.CONTACT_PATH)

    def to_login(self):
        return rx.redirect(path=Routes.LOGIN_PATH)

    def to_signup(self):
        return rx.redirect(path=Routes.SIGNUP_PATH)
