from typing import List

from .core import ArgosElement
from .line import ArgosLine


class ArgosDropdown(ArgosElement):
    def __init__(self, *, title: ArgosLine = None, items: List[ArgosLine] = None) -> None:
        super().__init__()

        self.title: ArgosLine = title
        self.items: List[ArgosLine] = items if items is not None else []

    def to_argos(self) -> str:
        output = []

        # Set the title
        if self.title is not None:
            output.append(self.title.to_argos())

        # Add the menu
        for item in self.items:
            output.append(f"--{item.to_argos()}")

        # Return everything on separate lines
        return '\n'.join(output)
