import abc


class ParserBase(abc.ABC):
    @abc.abstractmethod
    def serialize(self, candidates: list):
        pass
    @abc.abstractmethod
    def deserialize(self):
        pass
