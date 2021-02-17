import abc


class DataLoaderService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def identifier(self):
        pass

    @abc.abstractmethod
    def load(self):
        pass
