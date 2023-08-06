from abc import abstractmethod, ABC


class ArgosElement(ABC):
    @abstractmethod
    def to_argos(self) -> str:
        pass
