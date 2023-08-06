from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import List, Dict


class ArgosElement(ABC):
    @abstractmethod
    def to_argos(self) -> str:
        pass


class ArgosSeparator(ArgosElement):
    def to_argos(self) -> str:
        return "---"


@dataclass
class ArgosAttributeGroup:
    @property
    def attributes(self) -> Dict[str, str]:
        output = {}

        for field in fields(self):
            value = getattr(self, field.name)

            # Always skip on None, let Argos handle defaults
            if value is None:
                continue

            if issubclass(field.type, bool):
                output[field.name] = 'true' if value else 'false'
            elif issubclass(field.type, int):
                output[field.name] = str(value)
            elif issubclass(field.type, str):
                output[field.name] = value
            elif issubclass(field.type, ArgosAttributeGroup):
                output |= value.attributes
            else:
                raise TypeError(f"type '{field.type.__name__}' unsupported by pyargos-to-argos type conversion")

        return output


class ArgosAttributedElement(ArgosElement, ABC):
    def __init__(self, *, attribute_group: ArgosAttributeGroup) -> None:
        super().__init__()
        self.attribute_group = attribute_group

    def to_argos(self) -> str:
        attributes = self.attributes

        if attributes:
            return f"{self.content}|{' '.join(f'{key}={val}' for key, val in self.attributes.items())}"
        else:
            return self.content

    @property
    @abstractmethod
    def content(self) -> str:
        pass

    @property
    def attributes(self) -> Dict[str, str]:
        return self.attribute_group.attributes


class ArgosPlugin:
    def __init__(self, *, buttons: List[ArgosAttributedElement] = None, elements: List[ArgosElement] = None) -> None:
        super().__init__()

        self.buttons: List[ArgosAttributedElement] = buttons if buttons is not None else []
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
