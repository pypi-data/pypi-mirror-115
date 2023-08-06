from dataclasses import dataclass
from typing import Any, Optional

from pyargos.core import ArgosAttributeGroup, ArgosSeparator, ArgosPlugin, ArgosAttributedElement, ArgosElement


def test_attributes_inheritance():
    @dataclass
    class A(ArgosAttributeGroup):
        one: str = "ONE"

    @dataclass
    class B(A):
        two: str = "TWO"

    assert A().attributes == {'one': 'ONE'}
    assert B().attributes == {'one': 'ONE', 'two': 'TWO'}


def test_attributes_conversion():
    @dataclass
    class MultiClassedSubtype(ArgosAttributeGroup):
        zero: int = 0

    @dataclass
    class MultiClassedType(ArgosAttributeGroup):
        one: str = "ONE"
        two: int = 2
        false: bool = False
        none: Optional[Any] = None
        subclass: MultiClassedSubtype = MultiClassedSubtype()

    assert MultiClassedType().attributes == {'one': 'ONE', 'two': '2', 'false': 'false', 'zero': '0'}


def test_separator():
    assert ArgosSeparator().to_argos() == '---'


def test_attributed_element_none():
    class TestAttributedClass(ArgosAttributedElement):
        @property
        def content(self) -> str:
            return "test content"

    assert TestAttributedClass(attribute_group=ArgosAttributeGroup()).to_argos() == "test content"


def test_attributed_element_some():
    @dataclass
    class TestAttributeGroup(ArgosAttributeGroup):
        test: bool = True

    class TestAttributedElement(ArgosAttributedElement):
        def __init__(self, *, attribute_group: TestAttributeGroup) -> None:
            super().__init__(attribute_group=attribute_group)

        @property
        def content(self) -> str:
            return "test content"

    assert TestAttributedElement(attribute_group=TestAttributeGroup()).to_argos() == "test content|test=true"


def test_plugin_empty():
    assert ArgosPlugin().to_argos() == '---'


def test_plugin_full():
    class ButtonClass(ArgosAttributedElement):
        @property
        def content(self) -> str:
            return "test content"

    class ElementClass(ArgosElement):
        def to_argos(self) -> str:
            return "test output"

    plugin = ArgosPlugin(
        buttons=[ButtonClass(attribute_group=ArgosAttributeGroup()), ButtonClass(attribute_group=ArgosAttributeGroup())],
        elements=[ElementClass(), ElementClass()]
    )

    assert plugin.to_argos() == \
           "test content\n" \
           "test content\n" \
           "---\n" \
           "test output\n" \
           "test output"
