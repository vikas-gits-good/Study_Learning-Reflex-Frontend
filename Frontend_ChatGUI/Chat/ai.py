import os

import reflex as rx
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(".env")

OPAI_MODEL = "gpt-4o-mini"


def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


def llm_response(
    messages,
    model: str = "gpt-4o-mini",
) -> str:
    opai_clnt = get_client()
    completion = opai_clnt.chat.completions.create(
        model=model,
        messages=messages,
    )
    return completion.choices[0].message.content
