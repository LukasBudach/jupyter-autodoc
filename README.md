# Jupyter Autodoc Project
## Purpose
Provides functionality to automatically generate docstrings of the following format in jupyter notebooks.
```
def functionName(parameter1, parameter2):
    """ Function Description
    :param parameter1: parameter description
    :type parameter1: type of parameter
    :param parameter2: parameter description
    :type parameter2: type of parameter
    :returns: whether and what the function returns
    :rtype: type of returned value
    """
```
This is currently only possible for already saved notebooks, not while still editing the notebook. It is highly likely that this restriction will stay.

## Approach
Reads the ``.ipynb`` file as JSON, searches for code cells with function definitions (which are note commented out). Adds an auto-generated docstring for these functions and writes the JSON again as ``.ipynb``.

## TODOs

### Definitely required features
- [ ] Allow for overwriting existing notebook instead of generating new one
- [ ] Skip adding docstrings for already commented functions
- [ ] Analyze whether there actually is a return value
- [ ] Analyze whether errors are explicitly raised in a function, add them to docstring
- [ ] Use type hints in function definition to fill in type fields where possible

### Optional features if requested/needed
- [ ] Analyze existing comments for docstring compliance and extend/replace them accordingly
  - [ ] Replace comments completely if they are not compliant
  - [ ] Use already existing but incomplete docstrings and extend them instead of replacing
- [ ] Add nbdev-like tags to explicitly take into consideration or skip cells for the docstring documentation
 