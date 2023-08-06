# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['track']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.41,<2.0.0',
 'click>=8.0.0,<9.0.0',
 'rich>=12.6.0,<13.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['track-job = track.cli:entry']}

setup_kwargs = {
    'name': 'track-job-applications',
    'version': '1.0.0',
    'description': 'A CLI application to help you track job applications and provide metrics on them.',
    'long_description': "# Track Job Applications Docs\n\nA CLI application to help you track job applications and provide metrics on them.\n\n![MIT License](https://img.shields.io/github/license/Aditya-Gupta1/job-application-cli?color=green&style=flat-square)\n![Open Issues](https://img.shields.io/github/issues/Aditya-Gupta1/job-application-cli?color=dark-green&style=flat-square)\n![Good First Issues](https://img.shields.io/github/issues/Aditya-Gupta1/job-application-cli/good%20first%20issue?color=blue&style=flat-square)\n\nThis can help you answer questions like:\n\n- In how many companies have I been shortlisted yet?\n- What companies rejected my profile?\n- In how many companies I've given tech interviews?\n- In how many HR rounds I got rejected?\n- How many offers do I have? *Though you won't forget this one!*\n\nAnd the list goes on.\n\n![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)\n![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)\n![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-blue.svg?logoColor=white&style=for-the-badge&color=red)\n\n## Table of Contents\n\n* [Documentation](#documentation)\n* [Installation](#installation)\n* [Getting Started](#getting-started)\n* [Contributing](#contributing)\n* [Reach out](#reach-out)\n* [License](#license)\n\n## Documentation\n\nThe documentation for this project is created using [Mkdocs](https://www.mkdocs.org/)\nand deployed on [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages).\n\nYou can find the documentation here: https://aditya-gupta1.github.io/track-job-applications/\n\n>Markdown files that generates documentation are in `docs` folder. The website elements are generated from `docs` folder and moved to `gh-deploy` branch. It is from here that the GitHub pages picks up the files for deployment.\n\n## Installation\n\n**Prerequisites:** [Python](https://www.python.org/downloads/)\n\nRun the following command to install the application:\n```cmd\npip install track-job-applications\n```\n\n## Getting Started\n\n```commandline\n// add a job application\n> track-job add CompanyX SDE-1\n\n// display all the applications\n> track-job ls\n\n// update the application details\n> track-job update company <application-id> <new company name>\n\n// know more about any command\n> track-job <command> --help\n\n// know about all the commands available\n> track-job --help\n\n// get a report on all the applications\n> track-job report\n\n// get report on all the applications made within a date range\n> track-job report -s <start date in YYYY-MM-DD> -e <end date in YYYY-MM-DD>\n\n// total applications rejected\n> track-job report status rejected\n```\n\nRefer to the [commands](https://aditya-gupta1.github.io/track-job-applications/Commands/) section in the documentation for the list of commands available.\n\n> Note: All the commands have a `--start-date` or `-s` argument to mention the start date and `--end-date` or `-e` argument\n> to specify the end date, in case the command is to run for applications made within a date range.\n>  Also, the data model in which applications are stored can be found in [references](https://aditya-gupta1.github.io/track-job-applications/References/) section in the docs.\n\n## Contributing\n\nContributions for docs as well as code are welcomed. Head over to the [Contributing](https://github.com/Aditya-Gupta1/track-job-applications/blob/main/CONTRIBUTING.md) \nguidelines for steps to set up a development environment, contributing to code and contributing to docs.\n\n## Reach out\n\nFeel free to start a [discussion](https://github.com/Aditya-Gupta1/track-job-applications/discussions) on anything you want to suggest or have more clarity on.  \n\n## License\n\n[MIT License](https://github.com/Aditya-Gupta1/track-job-applications/blob/main/LICENSE.md)\n",
    'author': 'Aditya Gupta',
    'author_email': 'guptaaditya008@gmail.com',
    'maintainer': 'Aditya Gupta',
    'maintainer_email': 'guptaaditya008@gmail.com',
    'url': 'https://github.com/Aditya-Gupta1/track-job-applications',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
