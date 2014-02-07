from contextlib import closing
from src.operators import events
from src.operators import os_independency
from src.operators.os_independency import get_writer_according_to_os
from src.operators.translation.string_event_translation import EventsToStringTranslator


# def process_macros(events):
#     try:
#         translation = EventsToStringTranslator().translate_iterable(events)
#         process_translation(translation)
#     except KeyError:
#         pass
#
#
# def process_translation(translation):
#     print translation
#     if translation == "q":
#         with closing(get_writer_according_to_os()) as writer:
#             events_to_write = (
#                 events.KEY_BACKSPACE,
#                 events.KEY_BACKSPACE,
#                 events.KEY_Q,
#                 events.KEY_U,
#                 events.KEY_E,
#                 events.KEY_SPACE
#             )
#             writer.write_iterable(events_to_write)


if __name__ == "__main__":
    # writer = os_independency.get_writer_according_to_os()
    # translator = StringToEventsTranslator()
    # try:
    #     writer.write_iterable(translator.translate("hello world"))
    # finally:
    #     writer.close()

    reader = os_independency.get_reader_according_to_os()
    translator = EventsToStringTranslator()

    end_delimiters = frozenset((
        events.KEY_SPACE,
    ))

    pressed_events = []
    for event in reader.read_events():
        if event in end_delimiters:
            process_macros(pressed_events)
            del pressed_events[:]
        else:
            pressed_events.append(event)