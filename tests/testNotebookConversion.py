import unittest

import json

from argparse import Namespace
from pathlib import Path
from shutil import rmtree

from main import main


class TestNotebookConversion(unittest.TestCase):
    _tmpdir = None

    @classmethod
    def setUpClass(cls):
        cls._tmpdir = Path(f'tests/testdata/tmp/{cls.__name__}')

    @classmethod
    def tearDownClass(cls):
        rmtree(cls._tmpdir)

    def _comp_notebooks(self, path_expected, path_generated):
        """ Utility function, reading the two given notebooks (as JSON files) and comparing the cells they contain.
        Already contains assertions for these things, does not return the check result.

        :param path_expected: path to the expected/reference notebook
        :type path_expected: str or pathlike
        :param path_generated: path to the generated notebook
        :type path_generated: str or pathlike
        """
        with open(path_expected, 'r') as f:
            expected_nb = json.load(f)
        with open(path_generated, 'r') as f:
            generated_nb = json.load(f)

        self.assertEqual(
            len(expected_nb['cells']),
            len(generated_nb['cells']),
            f'The generated notebook had {generated_nb["cells"]} cells. Expected {expected_nb["cells"]} cells.'
        )

        for i in range(len(expected_nb)):
            self.assertDictEqual(
                expected_nb['cells'][i],
                generated_nb['cells'][i],
                f'Cell {i} differed in the generated and expected notebooks. \n'
                f'  Expected: {expected_nb["cells"][i]}\n  Generated: {generated_nb["cells"][i]}'
            )

    def test_notebook_converted_as_expected(self):
        args = Namespace(
            in_notebook=Path('tests/testdata/testNotebook.ipynb'),
            out_notebook=self._tmpdir / 'generatedNotebook.ipynb'
        )

        main(args)

        self._comp_notebooks(Path('tests/testdata/testNotebook_documented.ipynb'), args.out_notebook)


if __name__ == '__main__':
    unittest.main()
