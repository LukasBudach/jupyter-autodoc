from components import line_to_components, components_to_lines, components_to_blocks, blocks_to_lines


if __name__ == '__main__':
    lines = [
        '    print(Ping)',
        '    print(Pong)',
        '    def someTestFunction(param1, param2):  # this is my test function',
        '        """ Some comment, this will be multiline later on! ',
        '        :param param1: this is one of the parameters',
        '        :returns: param1 ',
        '        """  ',
        '        if param1:',
        '            print(param2)  # this is interesting, isnt it?',
        '        # we are almost done!',
        '        return param1',
        '    ',
        '    def multilineTestFunction(',
        '        param1, # amazing parameter',
        '        # now, the next parameter will be better!',
        '        param2',
        '    ):',
        '        print(param1)',
        '        print(param2)',
        '    ',
        '    print(Pong)',
        '    def nestedFunction():',
        '        print(Contains stuff)',
        '        def innerFunction(param):',
        '            """ Comment for inner function',
        '            multiline of course!',
        '            """',
        '            print(inner function party!)',
        '            return True',
        '        print(Outer function again!)'
    ]
    components = list()
    for i, line in enumerate(lines):
        comp = line_to_components(line, components[i-1] if i > 0 else None)
        if components is not None:
            components.append(comp)

    new_lines = components_to_lines(components)

    blocks = components_to_blocks(components)

    for b in blocks:
        b.add_docstring()

    block_new_lines = blocks_to_lines(blocks)

    print('\n'.join(block_new_lines))
