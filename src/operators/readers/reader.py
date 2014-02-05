import abc


class Reader(object):
    """
    Abstract class for all the reader operators.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read_events(self):
        """
        Iterable method that will produce events forever.
        """
        raise NotImplementedError()

    def close(self):
        pass
