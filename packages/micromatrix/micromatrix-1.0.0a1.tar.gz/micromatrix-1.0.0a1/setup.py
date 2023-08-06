# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['micromatrix']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'micromatrix',
    'version': '1.0.0a1',
    'description': 'A small Python module which adds a generalized matrix class, supporting many operations with no external dependencies',
    'long_description': '# MicroMatrix\n**This is an old unfinished project which I plan to work on soon.**\n\nMicroMatrix is a small Python module which adds a generalized `Matrix` class, supporting many operations with no external dependencies.\n\n**MicroMatrix Supports:**\n* Matrices of any size\n* Complex Numbers\n* Addition & Subtraction\n* Multiplication & Division\n* Integer Exponentiation\n* Transposition\n* Inverse & Determinant\n* Assignment Operators\n* And more!\n\n## Usage\n### Installation\nFlask Sitemapper requires Python 3.10 or newer. The latest version can be installed from PyPi with pip as shown below.\n```terminal\npip install micromatrix\n```\n\nNow you can import the `Matrix` class to use in your code.\n```python\nfrom micromatrix import Matrix\n\n# Creating a 3x2 matrix\nmy_matrix = Matrix([1, 2, 3], [4, 5, 6])\n```\n\n### Matrix Operations\nMicroMatrix supports many operations, including the standard Python mathematical operators and common matrix operations. These operations can be combined and used for complex calculations.\n\nKeep in mind that some operations may not be possible depending on the dimension and elements of your matrices. In that case, you will see a `ValueError` with a description such as:\n```terminal\nValueError: Operation requires a square matrix\n```\n\n#### Reversible Operations\n* `Matrix + int | float | complex | Matrix`\n* `Matrix - int | float | complex | Matrix`\n* `Matrix * int | float | complex | Matrix`\n* `Matrix / int | float | complex | Matrix`\n* `Matrix == Any`\n#### Non-Reversible Operations\n* `Matrix ** int`\n* `+ Matrix`\n* `- Matrix`\n* `~ Matrix`\n* `abs(Matrix)`\n* `len(Matrix)`\n* `str(Matrix)`\n\n#### Properties\n* `Matrix.identity`\n* `Matrix.transpose`\n* `Matrix.determinant`\n* `Matrix.invert`\n\n#### Methods\n* `Matrix.administer(function)`',
    'author': 'h-janes',
    'author_email': 'dev@hjanes.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
