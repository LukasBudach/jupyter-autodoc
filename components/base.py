import re

from .manager import ComponentManager


class BaseComponent:
    COMPONENTTYPE = 'BaseComponent'

    @classmethod
    def from_code(cls, code):
        return cls(code)

    def __init__(self, code):
        self._whitespace = code[:len(re.match(r'\s*', code, re.UNICODE).group(0))]
        self._code = code[len(re.match(r'\s*', code, re.UNICODE).group(0)):]
        self._incomplete = False
        self._component_id = ComponentManager.get_id()
        # for all partial components, in order to be able to sort them
        self._part_id = 0

    def __str__(self):
        return '{} -- {}'.format(self.COMPONENTTYPE, self._code)

    def __repr__(self):
        return self.__str__()

    def is_incomplete(self):
        return self._incomplete

    def to_code(self):
        return self._whitespace + self._code

    def with_id(self, component_id):
        ComponentManager.release_id(self._component_id)
        self._component_id = component_id
        return self

    def with_part_id(self, part_id):
        self._part_id = part_id
        return self

    def get_id(self):
        return self._component_id

    def get_part_id(self):
        return self._part_id

    def indent(self):
        return len(self._whitespace)

    def whitespace(self):
        return self._whitespace
