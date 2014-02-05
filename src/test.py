from evdev import ecodes, InputDevice, categorize, UInput, list_devices


def find_keyboard_input_device():
    devices = map(InputDevice, list_devices())
    for device in devices:
        if "keyboard" in device.name.lower():
            return device
    raise LookupError("No device found with 'keyboard' in it's name :(.")

if __name__ == "__main__":
    with UInput() as ui:
        ui.write(ecodes.EV_KEY, ecodes.KEY_A, 1)
        ui.write(ecodes.EV_KEY, ecodes.KEY_A, 0)
        ui.syn()



    # dev = find_keyboard_input_device()
    #
    # print(dev)
    #
    # for event in dev.read_loop():
    #     if event.type == ecodes.EV_KEY:
    #         print(categorize(event))




