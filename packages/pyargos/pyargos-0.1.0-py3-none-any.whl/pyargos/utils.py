from dataclasses import dataclass
from typing import Optional

from .core import ArgosAttributeGroup


@dataclass
class ArgosImage(ArgosAttributeGroup):
    image: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class ArgosAction(ArgosAttributeGroup):
    bash: Optional[str] = None
    terminal: Optional[bool] = None
    href: Optional[str] = None
    eval: Optional[str] = None
    refresh: Optional[bool] = None
