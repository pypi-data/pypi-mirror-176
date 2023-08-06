# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.gesetz']

package_data = \
{'': ['*']}

install_requires = \
['gesetze>=1.1,<2.0', 'pelican>=4.5,<5.0']

setup_kwargs = {
    'name': 'pelican-gesetze',
    'version': '0.1.0',
    'description': "Pelican plugin wrapper for 'py-gesetze'",
    'long_description': '# Pelican plugin for [`py-gesetze`](https://codeberg.org/S1SYPHOS/py-gesetze)\n\n`pelican-gesetze` links german legal norms, dependency-free & GDPR-friendly.\n\n\n## Installation\n\nIt\'s available from [PyPi](https://pypi.org/project/pelican-gesetze) using a package manager of your choice:\n\n```text\n# Using \'pip\'\npip install pelican-gesetze\n\n# Using \'poetry\'\npoetry add pelican-gesetze\n```\n\n\n## Getting started\n\nUsing `pelican-gesetze` is straightforward: After installing it, the jinja filter `gesetzify` is available:\n\n```html\n<p class="content">\n    {{ page.content | gesetzify }}\n</p>\n```\n\n\n## Configuration\n\nThe following settings need to be prepended by `GESETZE_` to work, eg for enabling full `title` attributes, define `GESETZE_TITLE_ATTRIBUTE = \'full\'` [in your settings](https://docs.getpelican.com/en/latest/settings.html#settings) (most likely `pelicanconf.py`).\n\n\n| Setting             | Type        | Default                                        | Description                                    |\n| ------------------- | ----------- | ---------------------------------------------- | ---------------------------------------------- |\n| `DRIVER_ORDER`      | `list|str`  | `[\'gesetze\', \'dejure\', \'buzer\', \'lexparency\']` | Controls providers (and their respective order |\n| `TITLE_ATTRIBUTE`   | `str|False` | `False`                                        | Controls `title` attribute                     |\n| `CUSTOM_ATTRIBUTES` | `dict`      | `{"target": "_blank"}`                         | Defines HTML attribute defaults                |\n\nFor more information, see [here](https://codeberg.org/S1SYPHOS/py-gesetze/#configuration).\n\n\n## Roadmap\n\n- [x] Update `README.md`\n- [ ] Add tests\n',
    'author': 'Digitalbüro',
    'author_email': 'post@digitalbuero.eu',
    'maintainer': 'Martin Folkers',
    'maintainer_email': 'hello@twobrain.io',
    'url': 'https://digitalbuero.eu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
