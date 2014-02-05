from src.operators import os_independency
from src.operators.translation.string_event_translation import EventsToStringTranslator

if __name__ == "__main__":
    # writer = os_independency.get_writer_according_to_os()
    # translator = StringToEventsTranslator()
    # try:
    #     writer.write_iterable(translator.translate("hello world"))
    # finally:
    #     writer.close()

    reader = os_independency.get_reader_according_to_os()
    translator = EventsToStringTranslator()

    for event in reader.read_events():
        print "Pressed %s" % translator.translate_event(event)

