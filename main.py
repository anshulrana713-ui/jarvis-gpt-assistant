from gui.interface import create_gui
from core.speech_engine import auto_greet
from core.listener import start_wake_listener

root, add_chat, entry, get_response=create_gui()

root.after(
    500,
    lambda: auto_greet(add_chat)
)

root.after(
    1500,
    lambda: start_wake_listener(
        root,
        add_chat,
        entry,
        get_response,
        auto_greet
    )
)

root.mainloop()