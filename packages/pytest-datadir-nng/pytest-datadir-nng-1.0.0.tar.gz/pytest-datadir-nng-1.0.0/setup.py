# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_datadir_nng']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.0.0,<8.0.0']

entry_points = \
{'pytest11': ['pytest_datadir_nng = pytest_datadir_nng']}

setup_kwargs = {
    'name': 'pytest-datadir-nng',
    'version': '1.0.0',
    'description': 'Fixtures for pytest allowing test functions/methods to easily retrieve test resources from the local filesystem.',
    'long_description': '---\ntitle: "datadir-nng plugin for pytest\n  [![pypi-badge](https://img.shields.io/pypi/v/pytest-datadir-nng.svg?){.align-middle}](https://pypi.python.org/pypi/pytest-datadir-nng)"\n---\n\nThe `datadir-nng` plugin for [pytest](http://pytest.org/) provides the\n`datadir` and `datadir_copy` fixtures which allow test functions to\neasily access resources in data directories. It was forked from the\n[pytest-datadir-ng plugin](https://github.com/Tblue/pytest-datadir-ng)\nand updates the code to use `pathlib.Path` rather than `py.path.local`\nand to support modern python versions (hence the \\"nng\\" part in its name \n\\-- as in \\"*next* next generation\\").\n\nThis plugin provides two fixtures:\n\n-   The [datadir](#datadir) fixture allows test functions and methods to\n    access resources in so-called \\"data directories\\".\n-   The [datadir_copy](#datadir_copy) fixture is similar to the\n    [datadir](#datadir) fixture, but it copies the requested resources\n    to a temporary directory first so that test functions or methods can\n    modify their resources on-disk without affecting other test\n    functions and methods.\n\n# Installation\n\nJust do:\n\n    pip install pytest-datadir-nng\n\n# The datadir fixture {#datadir}\n\nThe \\"datadir\\" fixture allows test functions and methods to access\nresources in so-called \\"data directories\\".\n\nThe fixture behaves like a dictionary. Currently, only retrieving items\nusing the `d[key]` syntax is supported. Things like iterators, `len(d)`\netc. are not.\n\nHow the fixture looks for resources is best described by an example. Let\nus assume the following directory structure for your tests:\n\n    tests/\n    +-- test_one.py\n    +-- test_two.py\n    +-- data/\n    |   +-- global.dat\n    +-- test_one/\n    |   +-- test_func/\n    |       +-- data.txt\n    +-- test_two/\n        +-- TestClass/\n            +-- test_method/\n                +-- strings.prop\n\nThe file `test_one.py` contains the following function:\n\n``` python\ndef test_func(datadir):\n    data_path = datadir["data.txt"]\n\n    # ...\n```\n\nThe file `test_two.py` contains the following class:\n\n``` python\nclass TestClass:\n    def test_method(self, datadir):\n        strings_path = datadir["strings.prop"]\n\n        # ...\n```\n\nWhen the `test_func()` function asks for the `data.txt` resource, the\nfollowing directories are searched for a file or directory named\n`data.txt`, in this order:\n\n-   `tests/test_one/test_func/`\n-   `tests/test_one/`\n-   `tests/data/test_one/test_func/`\n-   `tests/data/test_one/`\n-   `tests/data/`\n\nThe path to the first existing file (or directory) is returned as a\n`pathlib.Path` object. In this case, the returned path would be\n`tests/test_one/test_func/data.txt`.\n\nWhen the `test_method()` method asks for the `strings.prop` resource,\nthe following directories are searched for a file or directory with the\nname `strings.prop`, in this order:\n\n-   `tests/test_two/TestClass/test_method/`\n-   `tests/test_two/TestClass/`\n-   `tests/test_two/`\n-   `tests/data/test_two/TestClass/test_method/`\n-   `tests/data/test_two/TestClass/`\n-   `tests/data/test_two/`\n-   `tests/data/`\n\nHere, this would return the path\n`tests/test_two/TestClass/test_method/strings.prop`.\n\nAs you can see, the searched directory hierarchy is slighly different if\na *method* instead of a *function* asks for a resource. This allows you\nto load different resources based on the name of the test class, if you\nwish.\n\nFinally, if a test function or test method would ask for a resource\nnamed `global.dat`, then the resulting path would be\n`tests/data/global.dat` since no other directory in the searched\ndirectory hierarchy contains a file named `global.dat`. In other words,\nthe `tests/data/` directory is the place for global (or fallback)\nresources.\n\nIf a resource cannot be found in *any* of the searched directories, a\n`KeyError` is raised.\n\n# The datadir_copy fixture {#datadir_copy}\n\nThe \\"datadir_copy\\" fixture is similar to the [datadir](#datadir)\nfixture, but copies the requested resources to a temporary directory\nfirst so that test functions or methods can modify their resources\non-disk without affecting other test functions and methods.\n\nEach test function or method gets its own temporary directory and thus\nits own fresh copies of the resources it requests.\n\n**Caveat:** Each time a resource is requested using the dictionary\nnotation, a fresh copy of the resource is made. This also applies if a\ntest function or method requests the same resource multiple times. Thus,\nif you modify a resource and need to access the *modified* version of\nthe resource later, save its path in a variable and use that variable to\naccess the resource later instead of using the dictionary notation\nmultiple times:\n\n``` python\ndef test_foo(datadir_copy):\n    # This creates the initial fresh copy of data.txt and saves\n    # its path in the variable "resource1".\n    resource1 = datadir_copy["data.txt"]\n\n    # ...modify resource1 on-disk...\n\n    # You now want to access the modified version of data.txt.\n\n    # WRONG way: This will overwrite your modified version of the\n    #            resource with a fresh copy!\n    fh = open(datadir_copy["data.txt"], "rb")\n\n    # CORRECT way: This will let you access the modified version\n    #              of the resource.\n    fh = open(resource1, "rb")\n```\n',
    'author': 'jdidion',
    'author_email': 'github@didion.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jdidion/pytest-datadir-nng',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
