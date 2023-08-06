from dataclasses import dataclass

from .core import ArgosAttributedElement, ArgosAttributeGroup
from .utils import ArgosImage, ArgosAction


@dataclass
class ArgosLineAttributes(ArgosAttributeGroup):
    color: str = None
    iconName: str = None
    image: ArgosImage = None
    length: int = None
    trim: bool = None
    alternate: bool = None
    emojize: bool = None
    ansi: bool = None
    useMarkup: bool = None
    unescape: bool = None
    action: ArgosAction = None


class ArgosLine(ArgosAttributedElement):
    def __init__(self, *, text: str, attribute_group: ArgosLineAttributes) -> None:
        super().__init__(attribute_group=attribute_group)
        self.text = text

    @property
    def content(self) -> str:
        return self.text
