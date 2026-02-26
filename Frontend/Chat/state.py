import reflex as rx


class ChatState(rx.State):
    DID_SUBMT: bool = False

    @rx.var
    def user_form_submit(self) -> bool:
        return self.DID_SUBMT

    def handle_submit(self, form_data: dict = {}):
        self.DID_SUBMT = True
