from evdev import ecodes
from src.collection_utilities.dictionary_utils import invert_dictionary
from src.operators import events

_event_to_ecode_map = {
    events.KEY_A: ecodes.KEY_A,
    events.KEY_B: ecodes.KEY_B,
    events.KEY_C: ecodes.KEY_C,
    events.KEY_D: ecodes.KEY_D,
    events.KEY_E: ecodes.KEY_E,
    events.KEY_F: ecodes.KEY_F,
    events.KEY_G: ecodes.KEY_G,
    events.KEY_H: ecodes.KEY_H,
    events.KEY_I: ecodes.KEY_I,
    events.KEY_J: ecodes.KEY_J,
    events.KEY_K: ecodes.KEY_K,
    events.KEY_L: ecodes.KEY_L,
    events.KEY_M: ecodes.KEY_M,
    events.KEY_N: ecodes.KEY_N,
    events.KEY_O: ecodes.KEY_O,
    events.KEY_P: ecodes.KEY_P,
    events.KEY_Q: ecodes.KEY_Q,
    events.KEY_R: ecodes.KEY_R,
    events.KEY_S: ecodes.KEY_S,
    events.KEY_T: ecodes.KEY_T,
    events.KEY_U: ecodes.KEY_U,
    events.KEY_V: ecodes.KEY_V,
    events.KEY_W: ecodes.KEY_W,
    events.KEY_X: ecodes.KEY_X,
    events.KEY_Y: ecodes.KEY_Y,
    events.KEY_Z: ecodes.KEY_Z,

    events.KEY_0: ecodes.KEY_0,
    events.KEY_1: ecodes.KEY_1,
    events.KEY_2: ecodes.KEY_2,
    events.KEY_3: ecodes.KEY_3,
    events.KEY_4: ecodes.KEY_4,
    events.KEY_5: ecodes.KEY_5,
    events.KEY_6: ecodes.KEY_6,
    events.KEY_7: ecodes.KEY_7,
    events.KEY_8: ecodes.KEY_8,
    events.KEY_9: ecodes.KEY_9,

    events.KEY_SPACE: ecodes.KEY_SPACE,
    events.KEY_BACKSPACE: ecodes.KEY_BACKSPACE
}


class EventToEcodeTranslator(object):
    def translate(self, event):
        global _event_to_ecode_map
        return _event_to_ecode_map[event]


_ecode_to_event_map = invert_dictionary(_event_to_ecode_map)


class EcodeToEventTranslator(object):
    def translate(self, ecode):
        return _ecode_to_event_map[ecode]


