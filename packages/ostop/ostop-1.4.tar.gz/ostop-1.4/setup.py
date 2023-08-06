# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ostop']

package_data = \
{'': ['*']}

install_requires = \
['datetime>=4.7,<5.0',
 'hurryfilesize>=0.9,<0.10',
 'psutil>=5.9.3,<6.0.0',
 'schedule>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['my_package_cli = ostop.main:main']}

setup_kwargs = {
    'name': 'ostop',
    'version': '1.4',
    'description': 'Cross-Compatible Python implementation of top command.',
    'long_description': "# top\n\n[![build](../../actions/workflows/build.yml/badge.svg)](../../actions/)\n[![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)\n[![Commits: Conventional](https://img.shields.io/badge/Commits-Conventional-blue.svg)](https://www.conventionalcommits.org/en/v1.0.0/)\n\nA Cross-Platform Python implementation of 'top' command using Psutil.\n\n## What top Does\n\nTop is able to get most of the top information with the\nrestrictions that come with running it at the program level.\nDifferent statistics are shown based on\nthe operating system that this project is run on.\ntop works on MacOS, Linux, and Windows operating systems.\n\n## How to Get Started With top\n\nYou can get started with top by cloning the repository and running this command:\n\n``` python src/top.py ```\n\nin the base directory.\nLike the top command, this will run forever.\nYou can exit out of the program by entering a keyboard\ninterrupt or exiting your terminal altogether.\nYou can also specify the amount of times you want the program\nto run by giving a second integer input.\nFor example, you can run the program for one iteration\nby writing the command\n\n```python src/top.py 1```.\n\n## Running GatorGrade Checks\n\nThis repository is able to be automatically assessed using GatorGrade.\nThese checks can be run from the repository's base directory by running the command\n\n```gatorgrade --config config/gatorgrade.yml```\n\nin the base directory if you have GatorGrade installed.\nIf you do not have GatorGrade installed yet on your local machine,\nyou can install it by using the command\n\n```pip install gatorgrade```.\n\nThese checks ensure that files are formatted correctly\nwith proficient levels of polish and also run without crashing.\nGatorGrade checks are  useful both during and after development.\n",
    'author': 'Katherine Burgess',
    'author_email': '20burgessk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/burgess01/top',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
