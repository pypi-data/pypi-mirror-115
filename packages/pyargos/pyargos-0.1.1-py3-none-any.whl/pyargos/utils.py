from dataclasses import dataclass

from .core import ArgosAttributeGroup


@dataclass
class ArgosImage(ArgosAttributeGroup):
    image: str = None
    imageWidth: int = None
    imageHeight: int = None


class ArgosAction(ArgosAttributeGroup):
    bash: str = None
    terminal: bool = None
    href: str = None
    eval: str = None
    refresh: bool = None
