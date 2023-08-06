# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['choubun']

package_data = \
{'': ['*']}

install_requires = \
['MarkupSafe>=2.1.1,<3.0.0']

setup_kwargs = {
    'name': 'choubun',
    'version': '1.3.1',
    'description': 'A library for generating HTML and XML from Python using context managers',
    'long_description': '# Choubun 超文\n\n> (this is not recommended as a real way of generating HTML!)\n\n— [@contextlib.contextmanager](https://docs.python.org/3.5/library/contextlib.html#contextlib.contextmanager)\n\nChoubun is an alternative approach to templating engines.\nWhere a traditional template system has you writing your templates as separate files,\nChoubun allows you to mix Python control flow and HTML markup, all within Python\'s syntax.\n\nTo prevent injection vulnerabilities, Choubun uses [MarkupSafe](https://palletsprojects.com/p/markupsafe/) to escape unsafe text.\n`markupsafe.Markup` is also reexported as `Markup` and `M`.\n\n## How do I install it?\nChoubun is [available on PyPI](https://pypi.org/project/choubun/).\nUse `poetry add choubun` or your favorite dependency wrangler to start using Choubun in your project.\n\n## What does code using Choubun look like?\n```python\nfrom choubun import Node\ndoc = Node()\ndoc.raw(\'<!DOCTYPE html>\')\nwith doc.node(\'html\', lang=\'en\'):\n\twith doc.node(\'head\'):\n\t\tdoc.leaf(\'meta\', charset=\'utf-8\')\n\t\tfor k, v in dict(\n\t\t\tviewport="width=device-width, initial-scale=1",\n\t\t\treferrer=\'no-referrer\',\n\t\t).items():\n\t\t\tdoc.leaf(\'meta\', name=k, content=v)\n\twith doc.node(\'body\'):\n\t\tdoc.text("Page body")\n```\n',
    'author': 'Iridescence',
    'author_email': 'iridescent-aria+python@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/iridescent-aria/choubun',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
