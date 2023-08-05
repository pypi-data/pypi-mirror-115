# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfixfmt']

package_data = \
{'': ['*']}

install_requires = \
['autoflake>=1.3.1,<2.0.0', 'black>=19.10b0,<20.0', 'isort>=4.3.21,<5.0.0']

setup_kwargs = {
    'name': 'pyfixfmt',
    'version': '0.9.1',
    'description': 'Run several python fixers over a python file, to provide simple, deterministic code formatting.',
    'long_description': '# PyFixFmt\n\nA simple python formatter.\n\nJust removes unused imports (with [autoflake](https://github.com/myint/autoflake)), sorts imports (with [isort](https://github.com/PyCQA/isort)), and then formats the code (with [black](https://black.readthedocs.io/en/stable/)).\n\nMeant to make formatting of python code as deterministic as sanely possible.\n\n\n### Instructions\n\nTo install:\n\n`pip install pyfixfmt`\n\nTo run:\n\n\nRecommended way, since it should work from wherever\n\n`python -m pyfixfmt --file-glob <your file glob here> --verbose`\n\nOr, to run without installing\n\n`python pyfixfmt --file-glob <your file glob here> --verbose`\n\n\nfile-glob can be either a single file name or a normal unix glob.\n\n\n### Developing\n\nDevelop with [Poetry](https://python-poetry.org/).\n\nBuild with `poetry build`, and publish with `poetry publish`.',
    'author': 'TJ DeVries',
    'author_email': 'devries.timothyj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/untitled-ai/pyfixfmt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
