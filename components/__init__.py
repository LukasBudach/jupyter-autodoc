import re

from .comments import CommentComponent, MultilineCommentComponent
from .statements import StatementComponent


def line_to_components(code, prev_component):
    if prev_component is not None:
        if not isinstance(prev_component, tuple) and prev_component.is_incomplete():
            return prev_component.add_line(code)
        if isinstance(prev_component, tuple) and prev_component[0].is_incomplete():
            return prev_component[0].add_line(code)
    # first, check whether we are in any comment
    if '"""' in code:
        # return a docstring component
        return MultilineCommentComponent.from_code(code)
    elif '#' in code:
        # if the hashtag is the first non-whitespace character in the line of code // whole line must be comment
        if code.find('#') == len(re.match(r'\s*', code, re.UNICODE).group(0)):
            return CommentComponent.from_code(code)
        else:
            return StatementComponent.from_code(code), CommentComponent.from_code(code, inline=True)
    else:
        return StatementComponent.from_code(code)


def components_to_lines(components):
    lines = list()
    for c in components:
        if isinstance(c, tuple):
            line = c[0].to_code() + c[1].to_code()
        else:
            line = c.to_code()
        lines.append(line)
    return lines
