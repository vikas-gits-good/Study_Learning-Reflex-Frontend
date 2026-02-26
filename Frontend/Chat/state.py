import reflex as rx


class ChatState(rx.State):
    def handle_submit(self, form_data: dict = {}):
        print(f"{form_data = }")
