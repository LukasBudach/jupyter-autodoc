from .base import BaseComponent


class CommentComponent(BaseComponent):
    COMPONENTTYPE = 'CommentComponent'

    @classmethod
    def from_code(cls, code, inline=False):
        return cls(code, inline)

    def __init__(self, code, inline):
        super().__init__(code)
        self._code = code[code.find('#'):].strip()
        self._inline = inline
        if inline:
            self._whitespace = '  '


class MultilineCommentComponent(CommentComponent):
    COMPONENTTYPE = 'MultilineCommentComponent'

    def __init__(self, code, *args):
        super().__init__(code, False)
        self._code = code.strip()
        if self._code[-3:] != '"""':
            self._incomplete = True

    def add_line(self, code):
        self._code += code
        self._code = self._code.strip()
        if self._code[-3:] == '"""':
            self._incomplete = False

        return self
