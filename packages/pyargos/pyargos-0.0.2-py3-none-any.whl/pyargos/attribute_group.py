from abc import ABC, abstractmethod
from typing import Dict, Optional


class ArgosAttributeGroup(ABC):
    @property
    @abstractmethod
    def attributes(self) -> Dict[str, str]:
        return {}


class ArgosImage(ArgosAttributeGroup):
    def __init__(
            self,
            *,
            image: Optional[str] = None,
            width: Optional[int] = None,
            height: Optional[int] = None
    ) -> None:
        super().__init__()
        self.image = image
        self.width = width
        self.height = height

    @property
    def attributes(self) -> Dict[str, str]:
        output = super().attributes

        if self.image is not None:
            output['image'] = self.image

        if self.width is not None:
            output['imageWidth'] = str(self.width)

        if self.height is not None:
            output['imageHeight'] = str(self.height)

        return output


class ArgosAction(ArgosAttributeGroup):
    def __init__(
            self,
            *,
            bash: Optional[str] = None,
            terminal: Optional[bool] = None,
            href: Optional[str] = None,
            eval: Optional[str] = None,
            refresh: Optional[bool] = None,
    ) -> None:
        super().__init__()
        self.bash = bash
        self.terminal = terminal
        self.href = href
        self.eval = eval
        self.refresh = refresh

    @property
    def attributes(self) -> Dict[str, str]:
        output = super().attributes

        if self.bash is not None:
            output['bash'] = f'"{self.bash}"'

        if self.terminal is not None:
            output['terminal'] = "true" if self.terminal else "false"

        if self.href is not None:
            output['href'] = self.href

        if self.eval is not None:
            output['eval'] = self.eval

        if self.refresh is not None:
            output['refresh'] = "true" if self.refresh else "false"

        return output
