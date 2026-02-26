import reflex as rx
from pydantic import BaseModel

from .ai import llm_response


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
    CONVO_HIST: list[ChatMessage] = []

    @rx.var
    def user_form_submit(self) -> bool:
        return self.DID_SUBMT

    def handle_submit(self, form_data: dict = {}):
        user_message = form_data.get("HumanMessage", "")
        if user_message:
            self.DID_SUBMT = True
            self._append_message(user_message, False)
            yield

            self.sumr_convo()  # only runs if len(self.MESSAGES > 6) internally

            gpt_msgs = self.get_ai_messages()

            llm_rspn = llm_response(gpt_msgs)

            self.DID_SUBMT = False
            self._append_message(llm_rspn, True)
            yield

    def get_ai_messages(self):
        gpt_msgs = [
            {
                "role": "system",
                "content": """
                    You are an expert at creating food recipes.
                    Answer user queries about recipes and be concise.
                    Respond in markdown format thats easy to follow.
                """,
            }
        ]
        role = "user"
        for msg in self.MESSAGES:
            if not msg.is_bot:
                gpt_msgs.append(
                    {
                        "role": role,
                        "content": msg.message,
                    }
                )
        return gpt_msgs

    def sumr_convo(self):
        msgs = [
            {
                "role": "system",
                "content": """
                    You are a summarisation agent in a recipe conversation chatbot system.
                    Read though the conversation and summarise the conversation.
                    Make sure to include important details about user query, interest and
                    preferences. Limit the summary to less that 500 words.
                """,
            }
        ]
        if len(self.MESSAGES) > 6:
            for msg in self.MESSAGES[:-2]:
                msgs.append(
                    {
                        "role": "user" if not msg.is_bot else "assistant",
                        "content": msg.message,
                    }
                )
            sumr_resp = llm_response(msgs)
            self.MESSAGES = [
                ChatMessage(message=sumr_resp, is_bot=True),
                *self.MESSAGES[-2:],
            ]

    def _append_message(
        self,
        message,
        is_bot: bool = False,
    ):
        self.MESSAGES.append(
            ChatMessage(
                message=message,
                is_bot=is_bot,
            )
        )
        self.CONVO_HIST.append(
            ChatMessage(
                message=message,
                is_bot=is_bot,
            )
        )
