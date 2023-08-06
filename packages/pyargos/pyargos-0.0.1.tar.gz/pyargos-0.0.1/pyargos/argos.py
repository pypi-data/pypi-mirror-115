from abc import abstractmethod, ABC
from typing import List

from pyargos.attribute_element import ArgosButton
from pyargos.separator import ArgosSeparator


class ArgosElement(ABC):
    @abstractmethod
    def to_argos(self) -> str:
        pass


class ArgosPlugin:
    def __init__(self, *, buttons: List[ArgosButton] = None, elements: List[ArgosElement] = None) -> None:
        super().__init__()

        self.buttons: List[ArgosButton] = buttons if buttons is not None else []
        self.lines: List[ArgosElement] = elements if elements is not None else []

    def to_argos(self) -> str:
        output = []

        # Add the buttons
        for button in self.buttons:
            output.append(button.to_argos())

        # Add the button separator
        output.append(ArgosSeparator().to_argos())

        # Add the lines
        for line in self.lines:
            output.append(line.to_argos())

        # Return everything on separate lines
        return '\n'.join(output)
