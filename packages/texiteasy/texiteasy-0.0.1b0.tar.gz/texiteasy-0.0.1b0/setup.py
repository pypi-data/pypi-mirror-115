# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['texiteasy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'texiteasy',
    'version': '0.0.1b0',
    'description': 'This project contains tools to work with LaTeX.',
    'long_description': 'The `Python` module `TeXitEasy`\n===============================\n\n\n> **I beg your pardon for my english...**\n>\n> English is not my native language, so be nice if you notice misunderstandings, misspellings, or grammatical errors in my documents and codes.\n\n\nAbout `TeXitEasy`\n-----------------\n\nThis modules proposes some `Python` tools to work with `LaTeX`.\n\n\n<!-- :tutorial-START: -->\n<!-- :tutorial-END: -->\n\n\n<!-- :version-START: -->\n<!-- :version-END: -->\n',
    'author': 'Christophe BAL',
    'author_email': None,
    'maintainer': 'Christophe BAL',
    'maintainer_email': None,
    'url': 'https://github.com/projetmbc/tools-for-latex/tree/master/TeXitEasy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
