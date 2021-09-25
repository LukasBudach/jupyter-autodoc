from .blocks import CodeBlock, FunctionBlock
from .statements import FunctionDefinitionComponent


def components_to_blocks(components):
    if isinstance(components[0], tuple):
        base_indent = components[0][0].indent()
    else:
        base_indent = components[0].indent()
    blocks = list()
    open_block = None

    for comp in components:
        if isinstance(comp, tuple):
            working_comp = comp[0]
        else:
            working_comp = comp

        if (working_comp.indent() == base_indent) and (open_block is not None):
            if isinstance(open_block, CodeBlock):
                if isinstance(working_comp, FunctionDefinitionComponent):
                    blocks.append(open_block)
                    open_block = None
            elif isinstance(open_block, FunctionBlock) and open_block.body_empty():
                pass
            else:
                blocks.append(open_block)
                open_block = None

        if open_block is None:
            # open up a new block if none is open
            if isinstance(working_comp, FunctionDefinitionComponent):
                open_block = FunctionBlock()
            else:
                open_block = CodeBlock()
        # add the current component to the currently open block
        open_block.add_component(comp)
    blocks.append(open_block)

    for block in blocks:
        if isinstance(block, FunctionBlock):
            block._body_blocks = components_to_blocks(block.get_body())

    return blocks


def blocks_to_lines(blocks):
    lines = list()
    for b in blocks:
        lines.extend(b.to_lines())
    return lines
