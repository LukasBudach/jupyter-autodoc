import re
from .base import BaseComponent
from .comments import CommentComponent


class StatementComponent(BaseComponent):
    COMPONENTTYPE = 'StatementComponent'

    @classmethod
    def from_code(cls, code):
        first_non_whitespace = len(re.match(r'\s*', code, re.UNICODE).group(0))
        if code[first_non_whitespace : first_non_whitespace + 3] == 'def':
            return FunctionDefinitionComponent(code)
        else:
            return StatementComponent(code)

    def __init__(self, code):
        super().__init__(code)
        self._code = code[len(self._whitespace) : code.find('#') if code.find('#') > 0 else len(code)].strip()


class FunctionDefinitionComponent(StatementComponent):
    COMPONENTTYPE = 'FunctionDefinitionComponent'

    @classmethod
    def partial_from_code(cls, code):
        return cls(code, True)

    def __init__(self, code, partial_def=False):
        super().__init__(code)
        if not partial_def:
            # if we don't already know that this is only part of a function definition, we must be in the first line
            self._fname = self._code[self._code.find(' ') + 1: self._code.find('(')]
        if self._code.find(')') == - 1:
            self._incomplete = True
            self._params = self._code[self._code.find('(') + 1:].split(',')
        else:
            self._params = self._code[self._code.find('(') + 1: self._code.find(')')].split(',')
        self._params = [p.strip() for p in self._params if p not in ['', ' ']]

    def add_line(self, code):
        comment_start = code.find('#')
        first_non_whitespace = len(re.match(r'\s*', code, re.UNICODE).group(0))

        comment_component = None

        if comment_start == -1:
            function_def_component = FunctionDefinitionComponent.partial_from_code(code).with_id(self.get_id())
        elif comment_start > first_non_whitespace:
            function_def_component = FunctionDefinitionComponent.partial_from_code(code).with_id(self.get_id())
            comment_component = CommentComponent.from_code(code[comment_start:], inline=True)
        else:
            function_def_component = FunctionDefinitionComponent.partial_from_code('').with_id(self.get_id())
            comment_component = CommentComponent.from_code(code)

        if comment_component is None:
            return function_def_component
        else:
            return function_def_component, comment_component
