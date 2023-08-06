from dataclasses import dataclass
from typing import Optional

from .core import ArgosAttributedElement, ArgosAttributeGroup
from .utils import ArgosImage, ArgosAction


@dataclass
class ArgosLineAttributes(ArgosAttributeGroup):
    color: Optional[str] = None
    icon: Optional[str] = None
    image: Optional[ArgosImage] = None
    length: Optional[int] = None
    trim: Optional[bool] = None
    alternate: Optional[bool] = None
    emojize: Optional[bool] = None
    ansi: Optional[bool] = None
    markup: Optional[bool] = None
    unescape: Optional[bool] = None
    action: Optional[ArgosAction] = None


class ArgosLine(ArgosAttributedElement):
    def __init__(self, *, text: str, attribute_group: ArgosLineAttributes) -> None:
        super().__init__(attribute_group=attribute_group)
        self.text = text

    @property
    def content(self) -> str:
        return self.text
