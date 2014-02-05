import platform


def get_writer_according_to_os():
    if is_linux():
        return None
    elif is_windows():
        raise NotImplementedError("Windows is not currently implemented.")
    else:
        raise NotImplementedError("Unrecognized system.")


def get_reader_according_to_os():
    if is_linux():
        return None
    elif is_windows():
        raise NotImplementedError("Windows is not currently implemented.")
    else:
        raise NotImplementedError("Unrecognized system.")


def is_linux():
    return platform.system() == "Linux"


def is_windows():
    return platform.system() == "Windows"