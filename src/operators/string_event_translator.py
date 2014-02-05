from src.operators import events

_map_string_to_event = {
    "a": events.KEY_A,
    "b": events.KEY_B,
    "c": events.KEY_C,
    "d": events.KEY_D,
    "e": events.KEY_E,
    "f": events.KEY_F,
    "g": events.KEY_G,
    "h": events.KEY_H,
    "i": events.KEY_I,
    "j": events.KEY_J,
    "k": events.KEY_K,
    "l": events.KEY_L,
    "m": events.KEY_M,
    "n": events.KEY_N,
    "o": events.KEY_O,
    "p": events.KEY_P,
    "q": events.KEY_Q,
    "r": events.KEY_R,
    "s": events.KEY_S,
    "t": events.KEY_T,
    "u": events.KEY_U,
    "v": events.KEY_V,
    "w": events.KEY_W,
    "x": events.KEY_X,
    "y": events.KEY_Y,
    "z": events.KEY_Z,

    " ": events.KEY_SPACE
}


class StringToEventsTranslator(object):

    def translate(self, string):
        """
        @return: A list of events, corresponding to the translations of the individual
                 characters of the string.
        """
        string = string.lower()
        events_from_string = []
        for char in string:
            event = _map_string_to_event[char]
            events_from_string.append(event)
        return events_from_string