import reflex as rx

config = rx.Config(
    app_name="Frontend_ChatGUI",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
