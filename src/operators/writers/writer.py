import abc


class Writer(object):
    """
    Common interface for all the writer operators.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def write_iterable(self, events_iterable):
        """
        Consumes the members of the iterable, writing them one by one.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def write_event(self, event):
        raise NotImplementedError()

    @abc.abstractmethod
    def write_combo(self, events):
        """
        Writes all the events simultaniously. Useful for example for ctrl+something
        combinations.
        """
        raise NotImplementedError()

    def close(self):
        pass
