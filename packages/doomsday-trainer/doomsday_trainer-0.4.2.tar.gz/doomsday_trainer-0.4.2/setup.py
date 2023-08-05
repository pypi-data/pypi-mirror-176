# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doomsday_trainer']

package_data = \
{'': ['*']}

install_requires = \
['pysimplegui>=4.60.4,<5.0.0']

entry_points = \
{'console_scripts': ['doomsday-trainer = doomsday_trainer.trainer:main']}

setup_kwargs = {
    'name': 'doomsday-trainer',
    'version': '0.4.2',
    'description': 'Training tool for the Doomsday method.',
    'long_description': '# doomsday-trainer\n\nA simple GUI program for exercising the ability to calculate the day of week for\na given date (Gregorian calendar).\n\nThe name is taken from the\n[Doomsday rule](https://en.wikipedia.org/wiki/Doomsday_rule) - an algorithm\ndevised by [John Conway](https://en.wikipedia.org/wiki/John_Horton_Conway) in\n1973 for this specific purpose.\n\n## Installation\n\n```bash\npip install doomsday-trainer\n```\n\n## Usage\n\n```\nusage: doomsday-trainer [-h] [--start-year START_YEAR] [--end-year END_YEAR]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --start-year START_YEAR\n                        Start year [1800]\n  --end-year END_YEAR   End year [2099]\n```\n\n## Installation from source (using Poetry)\n\n```\ngit clone https://github.com/cbernander/doomsday-trainer.git\ncd doomsday-trainer\npoetry build\npip install dist/doomsday_trainer-*.whl\n```\n\n## Dependencies and external tools\n\n- Python 3.7+\n\n- [tkinter](https://docs.python.org/3/library/tkinter.html)\n\n- [Poetry](https://python-poetry.org/) for dependency management and packaging.\n\n- [tox](https://pypi.org/project/tox/) for testing.\n\n- [Black](https://black.readthedocs.io/en/stable/index.html) for code\n  formatting.\n\n- GUI built using [PySimpleGUI](https://www.pysimplegui.org/)\n',
    'author': 'Christofer Bernander',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cbernander/doomsday-trainer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
