import abc

class VisualizerService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def identifier(self):
        pass

    @abc.abstractmethod
    def visualize(self, graph):
        pass