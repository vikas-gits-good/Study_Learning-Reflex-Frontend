import reflex as rx
from ..gui import base_page
from ..navigation import Routes
from ..contact import ContactState, render_contact_list


@rx.page(
    route=Routes.CONTACT_ENTRIES_PATH,
    on_load=ContactState.list_entries,
)
def contact_entries_page() -> rx.Component:
    # print(ContactState.entries)
    my_child = rx.vstack(
        rx.heading("Contact Entries", size="6"),
        rx.text("List of user entry data"),
        rx.foreach(
            iterable=ContactState.entries,
            render_fn=render_contact_list,
        ),
        spacing="5",
        justify="start",
        align="center",
        min_height="85vh",
        id="my-child",
    )
    return base_page(child=my_child)
