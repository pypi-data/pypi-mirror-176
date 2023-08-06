# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jira_timesheet_cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'python-dateutil>=2.8.2,<3.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['book-time = book-time:main']}

setup_kwargs = {
    'name': 'jira-timesheet-cli',
    'version': '0.1.0',
    'description': 'A cli utility to book time in jira',
    'long_description': "# jira-timetracking-cli\n\nThis tool can be used to book times into JIRA issues. This tool uses the internal rest api (v3) of JIRA and therefore can be subject to change. Use it on your own risk!\n\n## Installation\n\nCreate new virtualenv `virtualenv ./venv`, activate it `source venv/bin/activate` install all requirements `pip install -r requirements.txt`. Then build the project using `pyinstaller book-time.spec`. Add `dist/book-time` to your `$PATH` and use it.\n\n## Usage\n\nBefore using the tool you need to specify the following environment variables:\n- JIRA_URL: The jira base url. Eg. `https://jira.test.com/`\n- JIRA_USER: Your JIRA user (eg. email address)\n- JIRA_TOKEN: Your API access token \n\nSee help for more information about the arguments: `book-time -help`. Examples:\n```\nbook-time -yesterday -ticket ABC-1234 -duration 3h15m -at 12:45\nbook-time -today -ticket ABC-1234 -duration 3h15m -at 12:45\nbook-time -ticket ABC-1234 -duration 3h15m -date 28-10-22 -now\nbook-time -ticket ABC-1234 -duration 3h15m -date 28-10-22 -at 12:45\n```\n\nIf you don't want to set a specific time and instead always book at the same time, you can just use an alias:\n```\nalias book-time='book-time -at 10:00'\n```\n\n## Completion\n\n`source <(book-time completion)`\n",
    'author': 'Yannick Habecker',
    'author_email': 'dev@y2g.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
