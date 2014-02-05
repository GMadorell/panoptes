

"""
Linux writer.
Read readme_installation in order to make it work.
"""
from evdev import UInput, ecodes
from src.operators.writers.event_to_ecode_translator import EventToEcodeTranslator
from src.operators.writers.writer import Writer


class EvdevWriter(Writer):

    def __init__(self):
        self.event_to_ecode_translator = EventToEcodeTranslator()
        self.ui = UInput()

    def write_event(self, event):
        ecode = self.event_to_ecode_translator.translate(event)
        self.ui.write(ecodes.EV_KEY, ecode, 1)
        self.ui.write(ecodes.EV_KEY, ecode, 0)
        self.ui.syn()

    def write_combo(self, *events):
        raise NotImplementedError()

    def close(self):
        self.ui.close()



