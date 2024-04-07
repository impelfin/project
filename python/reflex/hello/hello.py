import reflex as rx

from rxconfig import config


class State(rx.State):
    count: int = 0

    def increment(self):
        self.count += 1
        print(self.count)

    def decrement(self):
        self.count -= 1
        print(self.count)


def index():
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", font_size="2em"),
            rx.hstack(
                rx.button(
                    "Decrement",
                    color_scheme="red",
                    border_radius="1em",
                    on_click=State.decrement,
                ),
                rx.heading(State.count, font_size="2em"),
                rx.button(
                    "Increment",
                    color_scheme="green",
                    border_radius="1em",
                    on_click=State.increment,
                ),  
            ),      
        ),
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()
