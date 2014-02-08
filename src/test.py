from src.macro_listener import MacroListener
from src.operators import events
from src.operators.translation.event_ecode_translation import EventToEcodeTranslator

if __name__ == "__main__":
    listener = MacroListener()
    listener.add_macro_file_from_path("macro.pnp")
    listener.enter_reading_loop()

    # t = EventToEcodeTranslator()
    # t.translate(events.)