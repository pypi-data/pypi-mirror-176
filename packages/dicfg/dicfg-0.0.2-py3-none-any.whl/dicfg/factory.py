import operator
import re
from copy import deepcopy
from functools import reduce, singledispatchmethod
from importlib import import_module
from typing import Union


_REFERENCE_START_SYMBOL = "$"
_REFERENCE_MAP_SYMBOL = ":"
_REFERENCE_ATTRIBUTE_SYMBOL = "."

_OBJECT_KEY = "*object"
_RETURN_TYPE_KEY = "*return_type"


class _ObjectFactory:
    def __init__(self, config: dict):
        self._configuration = config

    def build_config(self):
        return self._build(self._configuration)

    @singledispatchmethod
    def _build(self, config: dict):
        return config

    @_build.register
    def _build_dict(self, config: dict):
        for key, value in config.items():
            if _is_object(value):
                config[key] = self._build_object(value)
            else:
                config[key] = self._build(value)
        return config

    @_build.register(list)
    @_build.register(tuple)
    def _build_list(self, config: Union[list, tuple]):
        for idx, item in enumerate(config):
            if _is_object(item):
                config[idx] = self._build_object(item)
            else:
                config[idx] = self._build(item)
        return config

    @_build.register
    def _build_str(self, config: str):
        if config.lower() == "none":
            return None
        if _REFERENCE_START_SYMBOL in config:
            return self._get_reference(reference=config)
        return config

    def _build_object(self, value: dict):
        kwargs = self._build(value)
        args = [] if "*args" not in kwargs else value.pop("*args")
        object_string = value.pop(_OBJECT_KEY)
        attribute = self._parse_object_str(object_string)

        if _RETURN_TYPE_KEY in value:
            return attribute
        return attribute(*args, **kwargs)

    def _parse_object_str(self, object_string: str):
        object_split = object_string.split(".")
        module_string = ".".join(object_split[:-1])
        attribute_string = object_split[-1]
        module = import_module(module_string)
        return getattr(module, attribute_string)

    def _get_reference(self, reference: str):
        matches = re.findall("\\${(.*?)}", reference)
        if matches == 1 or len(matches[0]) + 3 == len(reference):
            return self._object_interpolation(reference, matches)
        return self._string_interpolation(reference, matches)

    def _object_interpolation(self, reference, matches):
        reference = matches[0]
        references = reference.split(_REFERENCE_MAP_SYMBOL)
        reference = reduce(operator.getitem, references[:-1], self._configuration)
        attributes = references[-1].split(_REFERENCE_ATTRIBUTE_SYMBOL)
        reference = reference[attributes[0]]
        for attr in attributes[1:]:
            reference = getattr(reference, attr)
        return reference

    def _string_interpolation(self, reference, matches):
        for match in matches:
            _reference = self._configuration[match]
            match = "${" + match + "}"
            reference = reference.replace(match, str(_reference))
        return reference


def _is_object(value):
    return isinstance(value, dict) and _OBJECT_KEY in value


def build_config(config: dict):
    """builds config

    Args:
        config (dict): config to build

    Returns:
        dict: build config
    """

    return _ObjectFactory(deepcopy(config)).build_config()
