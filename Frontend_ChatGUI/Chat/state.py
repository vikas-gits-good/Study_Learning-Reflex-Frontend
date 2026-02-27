import reflex as rx
from pydantic import BaseModel

from Frontend_ChatGUI.models import ChatSession, ChatSessionMessageModel

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
    CHAT_SESN: ChatSession | None = None
    DID_SUBMT: bool = False
    MESSAGES: list[ChatMessage] = []
    CONVO_HIST: list[ChatMessage] = []

    @rx.var
    def user_form_submit(self) -> bool:
        return self.DID_SUBMT

    def on_load(self):
        if not self.CHAT_SESN:
            with rx.session() as db_sesn:
                obj = ChatSession()
                db_sesn.add(obj)
                db_sesn.commit()
                db_sesn.refresh(obj)
                self.CHAT_SESN = obj

    def handle_submit(self, form_data: dict = {}):
        user_message = form_data.get("HumanMessage", "")
        if user_message:
            self.DID_SUBMT = True
            self.append_message_to_gui(user_message, False)
            self.insert_db(content=user_message, role="user")
            yield

            self.sumr_convo()  # only runs if len(self.MESSAGES > 6) internally

            gpt_msgs = self.get_ai_messages()

            llm_rspn = llm_response(gpt_msgs)

            self.DID_SUBMT = False
            self.append_message_to_gui(llm_rspn, True)
            self.insert_db(content=llm_rspn, role="assistant")
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
                    Return only the summary and nothing else. Dont use markdown.
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

    def insert_db(self, content, role="uknown"):
        if not self.CHAT_SESN:
            return

        with rx.session() as ms_sesn:
            obj = ChatSessionMessageModel(
                session_id=self.CHAT_SESN.id,
                content=content,
                role=role,
            )
            ms_sesn.add(obj)
            ms_sesn.commit()

    def append_message_to_gui(
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
