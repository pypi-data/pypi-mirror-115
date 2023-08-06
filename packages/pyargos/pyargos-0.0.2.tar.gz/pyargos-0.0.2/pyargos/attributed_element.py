from abc import ABC, abstractmethod
from typing import Dict, Optional

from pyargos.element import ArgosElement
from pyargos.attribute_group import ArgosAttributeGroup, ArgosImage, ArgosAction


class ArgosAttributedElement(ArgosElement, ArgosAttributeGroup, ABC):
    def to_argos(self) -> str:
        return f"{self.content}|{' '.join(f'{key}={val}' for key, val in self.attributes.items())}"

    @property
    @abstractmethod
    def content(self) -> str:
        return ""


class ArgosLine(ArgosAttributedElement):
    def __init__(
            self,
            *,
            text: str,
            color: Optional[str] = None,
            icon: Optional[str] = None,
            image: Optional[ArgosImage] = None,
            length: Optional[int] = None,
            trim: Optional[bool] = None,
            alternate: Optional[bool] = None,
            emojize: Optional[bool] = None,
            ansi: Optional[bool] = None,
            markup: Optional[bool] = None,
            unescape: Optional[bool] = None,
            action: Optional[ArgosAction] = None
    ) -> None:
        super().__init__()
        self.text: Optional[str] = text
        self.trim = trim
        self.icon = icon
        self.ansi = ansi
        self.markup = markup
        self.emojize = emojize
        self.alternate = alternate
        self.length = length
        self.image = image
        self.unescape = unescape
        self.color = color
        self.action = action

    @property
    def content(self) -> str:
        return self.text

    @property
    def attributes(self) -> Dict[str, str]:
        output = super().attributes

        if self.trim is not None:
            output['trim'] = "true" if self.trim else "false"

        if self.icon is not None:
            output['icon'] = self.icon

        if self.ansi is not None:
            output['ansi'] = "true" if self.ansi else "false"

        if self.markup is not None:
            output['markup'] = "true" if self.markup else "false"

        if self.emojize is not None:
            output['emojize'] = "true" if self.emojize else "false"

        if self.alternate is not None:
            output['alternate'] = "true" if self.alternate else "false"

        if self.length is not None:
            output['length'] = str(self.length)

        if self.image is not None:
            output |= self.image.attributes

        if self.unescape is not None:
            output['unescape'] = "true" if self.unescape else "false"

        if self.color is not None:
            output['color'] = self.color

        if self.action is not None:
            output |= self.action.attributes

        return output


class ArgosButton(ArgosLine):
    def __init__(
            self,
            *,
            text: str,
            color: Optional[str] = None,
            icon: Optional[str] = None,
            image: Optional[ArgosImage] = None,
            length: Optional[int] = None,
            trim: Optional[bool] = None,
            alternate: Optional[bool] = None,
            emojize: Optional[bool] = None,
            ansi: Optional[bool] = None,
            markup: Optional[bool] = None,
            unescape: Optional[bool] = None,
            dropdown: Optional[bool] = None,
            action: Optional[ArgosAction] = None
    ) -> None:
        super().__init__(
            text=text,
            color=color,
            icon=icon,
            image=image,
            length=length,
            trim=trim,
            alternate=alternate,
            emojize=emojize,
            ansi=ansi,
            markup=markup,
            unescape=unescape,
            action=action
        )
        self.dropdown = dropdown

    @property
    def attributes(self) -> Dict[str, str]:
        output = super().attributes

        if self.dropdown is not None:
            output['dropdown'] = 'true' if self.dropdown else 'false'

        return output
