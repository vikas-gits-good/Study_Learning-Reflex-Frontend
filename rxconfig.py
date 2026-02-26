import os

import reflex as rx
from dotenv import load_dotenv

load_dotenv(".env")

config = rx.Config(
    app_name="Frontend_ChatGUI",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    db_url=os.getenv("DATABASE_URL", "sqlite:///reflex.db"),
)
