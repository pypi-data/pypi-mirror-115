from dataclasses import dataclass
from typing import Optional

from .line import ArgosLine, ArgosLineAttributes


@dataclass
class ArgosButtonAttributes(ArgosLineAttributes):
    dropdown: Optional[bool] = None


class ArgosButton(ArgosLine):
    def __init__(self, *, text: str, attribute_group: ArgosButtonAttributes) -> None:
        super().__init__(text=text, attribute_group=attribute_group)
