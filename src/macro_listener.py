from contextlib import closing
from src.operators import os_independency
from src.macros.macro_collection import MacroCollection
from src.macros.macro_file_parser import MacroFileParser
from src.operators import events
from src.operators.os_independency import get_writer_according_to_os
from src.operators.translation.string_event_translation import EventsToStringTranslator, StringToEventsTranslator


class MacroListener(object):

    DEFAULT_END_DELIMITERS = (
        events.KEY_SPACE,
    )

    DEFAULT_TRIGGERS = (
        events.KEY_CAPS_LOCK,
    )

    def __init__(self, end_delimiters=DEFAULT_END_DELIMITERS, triggers = DEFAULT_TRIGGERS):
        self.__delimiters = end_delimiters
        self.__triggers = triggers

        self.__reader = None
        self.__macro_collection = MacroCollection()
        self.__macro_file_parser = MacroFileParser()

    def add_macro_file_from_path(self, path):
        with file(path, "r") as macro_file:
            self.add_macro_file(macro_file)

    def add_macro_file(self, file_object):
        new_collection = self.__macro_file_parser.parse_file(file_object)
        new_macros = new_collection.get_macros()
        for new_macro in new_macros:
            self.__macro_collection.add(new_macro)

    def enter_reading_loop(self):
        try:
            self.__reader = os_independency.get_reader_according_to_os()
            self.__run_reading_loop()
        finally:
            self.__reader.close()

    def __run_reading_loop(self):
        pressed_events = []
        for event in self.__reader.read_events():
            if event in self.__triggers:
                self.__process_macro(pressed_events)
                del pressed_events[:]
            elif event in self.__delimiters or event is None:
                del pressed_events[:]
            else:
                pressed_events.append(event)

    def __process_macro(self, pressed_events):
        try:
            translation = EventsToStringTranslator().translate_iterable(pressed_events)
        except KeyError, key_error:
            print "KeyError while traslating in MacroListener#__process_macro: %s" % str(key_error)
            return
        self.__process_translated_macro(translation)

    def __process_translated_macro(self, translation):
        macro = self.__macro_collection.match(translation)
        if macro is not None:
            macro_text = macro.apply_declaration(translation)
            self.__write_macro(macro_text)

    def __write_macro(self, macro_text):
        print macro_text
        events_to_process = StringToEventsTranslator().translate(macro_text)

        with closing(get_writer_according_to_os()) as writer:
            writer.write_iterable(events_to_process)
