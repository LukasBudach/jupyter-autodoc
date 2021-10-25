import unittest

from components import components_to_lines, line_to_components
from components.statements import StatementComponent, FunctionDefinitionComponent, ReturnComponent
from components.comments import CommentComponent, MultilineCommentComponent


class TestComponentsSingleLine(unittest.TestCase):
    def test_line_to_components_function_complete(self):
        test_line = '    def aFunction(param):'
        components = line_to_components(test_line, None)
        self.assertIsInstance(components, tuple)
        self.assertEqual(1, len(components))
        self.assertIsInstance(components[0], FunctionDefinitionComponent)
        self.assertFalse(components[0].is_incomplete())
        self.assertEqual(test_line, components[0].to_code())

    def test_line_to_components_function_incomplete(self):
        test_line = '    def aFunction('
        components = line_to_components(test_line, None)
        self.assertIsInstance(components, tuple)
        self.assertEqual(1, len(components))
        self.assertIsInstance(components[0], FunctionDefinitionComponent)
        self.assertTrue(components[0].is_incomplete())
        self.assertEqual(test_line, components[0].to_code())

    def test_line_to_components_statement(self):
        test_line = '        if param1 == param2:'
        components = line_to_components(test_line, None)
        self.assertIsInstance(components, tuple)
        self.assertEqual(1, len(components))
        self.assertIsInstance(components[0], StatementComponent)
        self.assertNotIsInstance(components[0], FunctionDefinitionComponent)
        self.assertNotIsInstance(components[0], ReturnComponent)
        self.assertEqual(test_line, components[0].to_code())

    def test_line_to_components_return(self):
        test_line = '            return True'
        components = line_to_components(test_line, None)
        self.assertIsInstance(components, tuple)
        self.assertEqual(1, len(components))
        self.assertIsInstance(components[0], ReturnComponent)
        self.assertEqual(test_line, components[0].to_code())

    def test_line_to_components_inline_comment(self):
        test_line = '    print(Ping)  # a comment!'
        components = line_to_components(test_line, None)
        self.assertIsInstance(components, tuple)
        self.assertEqual(2, len(components))
        self.assertIsInstance(components[0], StatementComponent)
        self.assertIsInstance(components[1], CommentComponent)
        self.assertTrue(components[1].is_inline())
        self.assertEqual(test_line, components[0].to_code() + components[1].to_code())

    def test_line_to_components_inline_comment_respace(self):
        test_line = '    print(something) # a comment!'
        exptd_out = '    print(something)  # a comment!'
        components = line_to_components(test_line, None)
        self.assertIsInstance(components, tuple)
        self.assertEqual(2, len(components))
        self.assertIsInstance(components[1], CommentComponent)
        self.assertEqual(exptd_out, components[0].to_code() + components[1].to_code())

    def test_line_to_components_comment(self):
        test_line = '# a comment'
        components = line_to_components(test_line, None)
        self.assertIsInstance(components, tuple)
        self.assertEqual(1, len(components))
        self.assertIsInstance(components[0], CommentComponent)
        self.assertFalse(components[0].is_inline())
        self.assertEqual(test_line, components[0].to_code())

    def test_line_to_components_multiline_comment_complete(self):
        test_line = '    """ A complete multiline comment; can contain a # without issues"""'
        components = line_to_components(test_line, None)
        self.assertIsInstance(components, tuple)
        self.assertEqual(1, len(components))
        self.assertIsInstance(components[0], MultilineCommentComponent)
        self.assertFalse(components[0].is_incomplete())
        self.assertEqual(test_line, components[0].to_code())

    def test_line_to_components_multiline_comment_incomplete(self):
        test_line = '""" An incomplete multiline comment'
        components = line_to_components(test_line, None)
        self.assertIsInstance(components, tuple)
        self.assertEqual(1, len(components))
        self.assertIsInstance(components[0], MultilineCommentComponent)
        self.assertTrue(components[0].is_incomplete())
        self.assertEqual(test_line, components[0].to_code())


class TestComponentsMultipleLines(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sample_code = """print('Ping')
    print('Lets go')
    
    def uncommentedFunction(param1, param2):
        if param1 == param2:
            return True
        return False
    
    def multilineFunction(
        param1,
        # comment within function definition
        param2,  # may want to explain something about param 2 here?
        param3
    )
        print('I have neither comment nor return!)
        param3 = param1 * param2  # we don't actually need param3
    
    def outerFunction(param1):
        \"\"\" This function has a docstring, albeit incomplete.
        # Comments within a docstring are only part of it!
        :param param1: this is a parameter
        \"\"\"
        print('An inner function will be defined!')
        def innerFunction(param):
            print('I have no docstring')
            # simply return the input parameter
            return param
        print('Now I am happy with it.')
    """
        cls.code_lines = cls.sample_code.split('\n')

    def test_sample_lines_and_code_match(self):
        self.assertEqual(self.sample_code, '\n'.join(self.code_lines))

    def test_sample_lines_to_components(self):
        components = list()
        for i, line in enumerate(self.code_lines):
            components.append(line_to_components(line, None if i == 0 else components[i-1]))

        expected_types = [
            (StatementComponent,),
            (StatementComponent,),
            (StatementComponent,),  # empty line
            (FunctionDefinitionComponent,),
            (StatementComponent,),
            (ReturnComponent,),
            (ReturnComponent,),
            (StatementComponent,),  # empty line
            (FunctionDefinitionComponent,),
            (FunctionDefinitionComponent,),
            (FunctionDefinitionComponent, CommentComponent),
            (FunctionDefinitionComponent, CommentComponent),
            (FunctionDefinitionComponent,),
            (FunctionDefinitionComponent,),
            (StatementComponent,),
            (StatementComponent, CommentComponent),
            (StatementComponent,),  # empty line
            (FunctionDefinitionComponent,),
            (MultilineCommentComponent,),
            (MultilineCommentComponent,),
            (MultilineCommentComponent,),
            (MultilineCommentComponent,),
            (StatementComponent,),
            (FunctionDefinitionComponent,),
            (StatementComponent,),
            (CommentComponent,),
            (ReturnComponent,),
            (StatementComponent,),
            (StatementComponent, )  # empty line
        ]

        for i, component in enumerate(components):
            self.assertEqual(len(expected_types[i]), len(component))
            self.assertIsInstance(component[0], expected_types[i][0], 'Expected instance was {}, got {} for line {}'.format(expected_types[i][0], type(component[0]), i))
            if len(expected_types[i]) > 1:
                self.assertIsInstance(component[1], expected_types[i][1])

    def test_conversion_to_and_from_components(self):
        components = list()
        for i, line in enumerate(self.code_lines):
            components.append(line_to_components(line, None if i == 0 else components[i - 1]))

        self.assertEqual(self.code_lines, components_to_lines(components))


if __name__ == '__main__':
    unittest.main()
