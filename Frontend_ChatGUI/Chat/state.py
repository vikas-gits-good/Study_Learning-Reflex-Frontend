import asyncio

import reflex as rx
from pydantic import BaseModel


class MessageStyle(BaseModel):
    display: str = "inline-block"
    padding: str = "0.5em"
    border_radius: str = "15px"
    max_width: list[str] = ["30em", "30em", "50em", "50em", "50em", "50em"]


class ChatMessage(BaseModel):
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

            await asyncio.sleep(2)
            self.DID_SUBMT = False
            self._append_message(user_message, True)
            yield

    def _append_message(self, message, is_bot: bool = False):
        # if self.DID_SUBMT:
        self.MESSAGES.append(
            ChatMessage(
                message=message,
                is_bot=is_bot,
            )
        )
