import re


class BaseComponent:
    COMPONENTTYPE = 'BaseComponent'

    @classmethod
    def from_code(cls, code):
        return cls(code)

    def __init__(self, code):
        self._whitespace = code[:len(re.match(r'\s*', code, re.UNICODE).group(0))]
        self._code = code[len(re.match(r'\s*', code, re.UNICODE).group(0)):]
        self._incomplete = False

    def __str__(self):
        return '{} -- {}'.format(self.COMPONENTTYPE, self._code)

    def __repr__(self):
        return self.__str__()

    def is_incomplete(self):
        return self._incomplete

    def to_code(self):
        return self._whitespace + self._code
