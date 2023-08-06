import importlib
import inspect
import os
import pkgutil
import sys

from .attribute_group import ArgosAttributeGroup
from .element import ArgosElement
from .plugin import ArgosPlugin

_expose_from = (ArgosAttributeGroup, ArgosElement)

# lmao
for _, name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
    module = importlib.import_module('.' + name, package=__name__)

    for attr in dir(module):
        attribute = getattr(module, attr)

        if inspect.isclass(attribute) and any(issubclass(attribute, parent) and attribute != parent for parent in _expose_from):
            setattr(sys.modules[__name__], attribute.__name__, attribute)

del importlib, inspect, os, pkgutil, sys
del _expose_from
