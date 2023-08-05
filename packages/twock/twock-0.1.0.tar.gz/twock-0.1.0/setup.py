# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twock']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'loguru>=0.5.3,<0.6.0',
 'ndjson>=0.3.1,<0.4.0',
 'pandas>=1.3.1,<2.0.0',
 'twarc>=2.3.10,<3.0.0']

entry_points = \
{'console_scripts': ['twock = twock.twock:cli']}

setup_kwargs = {
    'name': 'twock',
    'version': '0.1.0',
    'description': 'Ping/Knock a list of tweets to enquire their status (deleted/available/...) #twockknock',
    'long_description': "# twock\n\nPing/knock a list of tweets to enquire their status (deleted/available/...) #twockknock\n\n## Usage\n\n### Knocking Tweets\n\n```\ntwock knock [OPTIONS] TWEETFILE\n\n  Ping (knock) a list of tweets. Expects file path to CSV with `id` column.\n\nOptions:\n  --outpath TEXT    Path to output file, will be prefixed with today's date.\n                    Default: `errors.ndjson`\n  --tkpath TEXT     Path to Twitter API v2 bearer token YAML file. Default:\n                    `bearer_token.yaml`\n  --sample INTEGER  If given, sample INTEGER number of tweets only\n  --help            Show this message and exit.\n```\n\n## Developer Install\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Clone repository\n3. In the cloned repository's root directory run `poetry install`\n4. Run `poetry shell` to start development virtualenv\n5. Run `twacapic` to enter API keys. Ignore the IndexError.\n6. Run `pytest` to run all tests\n",
    'author': 'Felix Victor Münch',
    'author_email': 'f.muench@leibniz-hbi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Leibniz-HBI/twock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
