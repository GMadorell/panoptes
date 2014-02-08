

"""
Linux writer.
Read readme_installation in order to make it work.
"""
from evdev import UInput, ecodes
from src.operators.translation.event_ecode_translation import EventToEcodeTranslator
from src.operators.writers.writer import Writer


class EvdevWriter(Writer):

    def __init__(self):
        self.event_to_ecode_translator = EventToEcodeTranslator()
        self.ui = UInput()

    def write_iterable(self, events_iterable):
        for event in events_iterable:
            if isinstance(event, list):
                self.write_combo(event)
            else:
                self.__buffer_event(event)
        self.ui.syn()

    def write_event(self, event):
        self.__buffer_event(event)
        self.ui.syn()

    def __buffer_event(self, event):
        ecode = self.event_to_ecode_translator.translate(event)
        self.ui.write(ecodes.EV_KEY, ecode, 1)
        self.ui.write(ecodes.EV_KEY, ecode, 0)

    def write_combo(self, events):
        for event in events:
            ecode = self.event_to_ecode_translator.translate(event)
            self.ui.write(ecodes.EV_KEY, ecode, 1)
            self.ui.syn()
        for event in reversed(events):
            ecode = self.event_to_ecode_translator.translate(event)
            self.ui.write(ecodes.EV_KEY, ecode, 0)
            self.ui.syn()

    def close(self):
        self.ui.close()



