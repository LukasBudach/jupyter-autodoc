from .comments import CommentComponent, MultilineCommentComponent
from .component_conversions import components_to_lines
from .statements import FunctionDefinitionComponent, ReturnComponent


SORTKEY_PARTS = lambda c: c[0].get_part_id() if isinstance(c, tuple) else c.get_part_id()
SORTKEY_IDS = lambda c: c[0].get_id() if isinstance(c, tuple) else c.get_id()


class FunctionBlock:
    def __init__(self):
        self._definition_components = list()
        self._docstring_components = list()
        self._body_components = list()
        self._body_blocks = list()

    def body_empty(self):
        return len(self._body_components) == 0

    def get_body(self):
        return sorted(self._body_components, key=SORTKEY_IDS)

    def contains_return(self):
        for c in reversed(self._body_components):
            if isinstance(c, ReturnComponent):
                return True
        return False

    def add_component(self, component):
        if isinstance(component, tuple):
            working_component = component[0]
        else:
            working_component = component
        if isinstance(working_component, FunctionDefinitionComponent) and ((len(self._definition_components) == 0) or self._definition_components[-1][0].is_incomplete()):
            self._definition_components.append(component)
        elif isinstance(working_component, MultilineCommentComponent) and (len(self._body_components) == 0):
            self._docstring_components.append(component)
        else:
            self._body_components.append(component)

    def add_docstring(self):
        if len(self._docstring_components) > 0:
            return

        function_params = list()
        fname = None
        whitespace = self._body_components[0][0].whitespace()

        for fdef_component in self._definition_components:
            function_params.extend(fdef_component[0].get_params())
            fname = fdef_component[0].get_func_name() if fdef_component[0].get_func_name() is not None else fname

        self._docstring_components.append((CommentComponent.from_code('{}# TODO: Fill out auto-generated docstring'.format(self._definition_components[0][0].whitespace())),))
        self._docstring_components.append((MultilineCommentComponent.from_code('{}""" Description of what function {} does. Can be multiline.'.format(whitespace, fname)),))
        for p in function_params:
            self._docstring_components.append(self._docstring_components[-1][0].add_line('{ws}:param {param}: Parameter description for {param}'.format(ws=whitespace, param=p)))
            self._docstring_components.append(self._docstring_components[-1][0].add_line('{ws}:type {param}: Type of {param}'.format(ws=whitespace, param=p)))
        if self.contains_return():
            self._docstring_components.append(self._docstring_components[-1][0].add_line('{}:returns: What does the function return?'.format(whitespace)))
            self._docstring_components.append(self._docstring_components[-1][0].add_line('{}:rtype: Type of the return value'.format(whitespace)))
        self._docstring_components.append(self._docstring_components[-1][0].add_line('{}"""'.format(whitespace)))

        for bb in self._body_blocks:
            bb.add_docstring()

    def to_lines(self):
        self._definition_components = sorted(self._definition_components, key=SORTKEY_PARTS)
        self._docstring_components = sorted(self._docstring_components, key=SORTKEY_PARTS)
        body_lines = list()
        for bb in self._body_blocks:
            body_lines.extend(bb.to_lines())
        return components_to_lines(self._definition_components + self._docstring_components) + body_lines


class CodeBlock:
    def __init__(self):
        self._components = list()

    def add_docstring(self):
        pass

    def add_component(self, component):
        self._components.append(component)

    def to_lines(self):
        self._components = sorted(self._components, key=SORTKEY_IDS)
        return components_to_lines(self._components)
