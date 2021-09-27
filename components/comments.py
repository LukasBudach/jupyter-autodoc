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

    def is_inline(self):
        return self._inline


class MultilineCommentComponent(CommentComponent):
    COMPONENTTYPE = 'MultilineCommentComponent'

    def __init__(self, code, *args):
        super().__init__(code, False)
        self._code = code.strip()
        if self._code[-3:] != '"""':
            self._incomplete = True

    def add_line(self, code):
        return (MultilineCommentComponent.from_code(code).with_id(self.get_id()).with_part_id(self._part_id + 1),)

    def is_incomplete(self):
        return self._incomplete
