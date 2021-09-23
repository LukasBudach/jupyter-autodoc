import argparse
import json
import re

from pathlib import Path


class Cell:
    CELLTYPE = 'Cell'

    def __init__(self, celldict):
        self._celldict = celldict

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{} with lines {}'.format(self.CELLTYPE, self._celldict['source'])

    def to_specific_celltype(self):
        if self._celldict['cell_type'] == 'code':
            return CodeCell(self._celldict).to_specific_celltype()
        return self


class CodeCell(Cell):
    CELLTYPE = 'Code'

    def to_specific_celltype(self):
        if self.contains_function_definition():
            return FunctionCell(self._celldict)
        return self

    def contains_function_definition(self):
        for line in self._celldict['source']:
            if re.search(r'def', line) and not re.match(r'\t* *#.*def', line):
                return True
        return False


class FunctionCell(CodeCell):
    CELLTYPE = 'Code with function definition'

    def __init__(self, celldict):
        super().__init__(celldict)
        self._function_lines = list()

    def get_function_definitions(self):
        defs = list()
        incomplete_def = False
        open_def = list()
        for i, line in enumerate(self._celldict['source']):
            if incomplete_def:
                open_def.append(line)
                if line.find(')') != -1:
                    incomplete_def = False
                    defs.append(''.join(open_def).replace('\n', ''))
                    open_def = list()
                    self._function_lines.append(i + 1)
            if re.search(r'def', line) and not re.match(r'\t* *#.*def', line):
                if line.find(')') == -1:
                    incomplete_def = True
                    open_def.append(line)
                else:
                    defs.append(line)
                    self._function_lines.append(i + 1)
        return [FunctionDefinition(d) for d in defs]

    def insert_function_docstrings(self, docstrings):
        new_source = self._celldict['source'][:self._function_lines[0]]
        for i, docstring in enumerate(docstrings):
            new_source.append(docstring)
            if i < (len(docstrings) - 1):
                new_source.extend(self._celldict['source'][self._function_lines[i] : self._function_lines[i + 1]])
            else:
                new_source.extend(self._celldict['source'][self._function_lines[i] : ])

        self._celldict['source'] = new_source


class FunctionDefinition:
    def __init__(self, def_line):
        code_start = def_line.find('def')
        self._whitespace = def_line[:code_start]
        self._fname = def_line[def_line.find(' ', code_start) + 1 : def_line.find('(')]
        self._params = def_line[def_line.find('(') + 1 : def_line.find(')')].split(',')
        self._params = [p.strip() for p in self._params if p not in ['', ' ']]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Function definition: {}'.format(str(self.__dict__))

    def generate_docstring(self):
        docstr = '{}# TODO: Fill out auto-generated docstring\n'.format(self._whitespace)
        docstr += '    {}""" Description of what function {} does. Can be multiline.\n'.format(self._whitespace, self._fname)
        for p in self._params:
            docstr += '    {ws}:param {param}: Parameter description for {param}\n'.format(ws=self._whitespace, param=p)
            docstr += '    {ws}:type {param}: Type of {param}\n'.format(ws=self._whitespace, param=p)
        docstr += '    {}:returns: What does the function return?\n'.format(self._whitespace)
        docstr += '    {}:rtype: Type of the return value\n'.format(self._whitespace)
        docstr += '    {}"""\n'.format(self._whitespace)
        return docstr


def load_cells(fpath):
    with open(fpath, 'r') as f:
        jupyter_dict = json.load(f)
    return [Cell(c).to_specific_celltype() for c in jupyter_dict['cells']]


def write_updated_cells(in_fpath, out_fpath, cells):
    with open(in_fpath, 'r') as f:
        jupyter_dict = json.load(f)

    jupyter_dict['cells'] = [c._celldict for c in cells]

    with open(out_fpath, 'w') as f:
        json.dump(jupyter_dict, f, indent=1)


def main(args):
    cells = load_cells(args.in_notebook)
    for c in cells:
        if isinstance(c, FunctionCell):
            function_definitions = c.get_function_definitions()
            docstrings = [fd.generate_docstring() for fd in function_definitions]
            c.insert_function_docstrings(docstrings)

    out_notebook = args.in_notebook.parent / '{}_documented.ipynb'.format(args.in_notebook.stem)
    write_updated_cells(args.in_notebook, out_notebook, cells)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--in-notebook', type=Path)

    main(parser.parse_args())
