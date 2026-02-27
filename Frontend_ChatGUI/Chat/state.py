import reflex as rx
import sqlmodel
from pydantic import BaseModel

from Frontend_ChatGUI.models import ChatSession, ChatSessionMessageModel
from Frontend_ChatGUI.Navigation import Routes

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
    NOT_FOUND: bool | None = None
    DID_SUBMT: bool = False
    MESSAGES: list[ChatMessage] = []
    CONVO_HIST: list[ChatMessage] = []
    # INVALID_LOOKUP: bool = False

    @rx.var
    def user_form_submit(self) -> bool:
        return self.DID_SUBMT

    def get_session_id(self) -> int:
        return int(self.router.url.path.split("/")[-1])

    def create_new_chat_sesn(self):
        with rx.session() as db_sesn:
            obj = ChatSession()
            db_sesn.add(obj)
            db_sesn.commit()
            db_sesn.refresh(obj)
            self.CHAT_SESN = obj
            return obj

    def clean_n_start_new(self):
        self.clear_gui()
        self.create_new_chat_sesn()
        yield

    def clear_gui(self):
        self.CHAT_SESN = None
        self.NOT_FOUND = None
        self.DID_SUBMT = False
        self.MESSAGES = []
        self.CONVO_HIST = []

    def get_sesn_from_db(self, sesn_id: int):
        if not sesn_id:
            sesn_id = self.get_session_id()

        self.clear_gui()

        with rx.session() as db_sesn:
            sql_stm = sqlmodel.select(ChatSession).where(ChatSession.id == sesn_id)
            result = db_sesn.exec(sql_stm).one_or_none()
            if not result:
                self.NOT_FOUND = True
            else:
                self.NOT_FOUND = False

            self.CHAT_SESN = result

            for msg in result.messages:
                self.append_message_to_gui(
                    message=msg.content,
                    is_bot=False if msg.role == "user" else True,
                )

    def create_new_n_redirect(self):
        self.clear_gui()
        obj = self.create_new_chat_sesn()
        return rx.redirect(f"{Routes.CHAT}/{obj.id}")

    def on_detail_load(self):
        sesn_id = self.get_session_id()
        if isinstance(sesn_id, int):
            self.get_sesn_from_db(sesn_id)

    def on_load(self):
        self.clear_gui()
        self.create_new_chat_sesn()

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
