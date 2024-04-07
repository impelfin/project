import reflex as rx

class ChatappConfig(rx.Config):
    pass

config = ChatappConfig(
    app_name="chatapp",
    frontend_port=3000,
)