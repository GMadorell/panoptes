from evdev import InputDevice, list_devices, ecodes, categorize
from src.operators.readers.reader import Reader
from src.operators.translation.event_ecode_translation import EcodeToEventTranslator


class EvdevReader(Reader):

    def __init__(self):
        self.__device = self.__find_keyboard_input_device()
        self._ecode_to_event_trans = EcodeToEventTranslator()

    def __find_keyboard_input_device(self):
        devices = map(InputDevice, list_devices())
        for device in devices:
            if "keyboard" in device.name.lower():
                return device
        raise LookupError("No device found with 'keyboard' in it's name :(.")

    def read_events(self):
        for evdev_event in self.__device.read_loop():
            if evdev_event.type == ecodes.EV_KEY:
                key_event = categorize(evdev_event)
                if key_event.keystate == 0:
                    ecode = key_event.scancode
                    event = self._ecode_to_event_trans.translate(ecode)
                    yield event

    def close(self):
        self.__device.close()