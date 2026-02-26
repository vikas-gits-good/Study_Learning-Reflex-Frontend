import asyncio

import reflex as rx


class ChatMessage(rx.Base):
    message: str
    is_bot: bool = False


class ChatState(rx.State):
    DID_SUBMT: bool = False
    MESSAGES: list[ChatMessage] = []

    @rx.var
    def user_form_submit(self) -> bool:
        return self.DID_SUBMT

    async def handle_submit(self, form_data: dict = {}):
        user_message = form_data.get("HumanMessage", "")
        if user_message:
            self.DID_SUBMT = True
            self._append_message(user_message, False)
            yield

            await asyncio.sleep(4)
            self.DID_SUBMT = False
            self._append_message(user_message, True)
            yield

    def _append_message(self, message, is_bot: bool = False):
        self.MESSAGES.append(
            ChatMessage(
                message=message,
                is_bot=is_bot,
            )
        )
