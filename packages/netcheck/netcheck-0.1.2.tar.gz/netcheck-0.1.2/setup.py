# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netcheck']

package_data = \
{'': ['*']}

install_requires = \
['dnspython>=2.2.1,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['netcheck = netcheck.cli:app']}

setup_kwargs = {
    'name': 'netcheck',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Network Health Check\n\nConfigurable command line application that can be used to test network conditions are as expected.\n\nVery early work in progress version!\n\n## Quickstart\n\n\n### Installation\n\n```\npip install netcheck\n```\n\n\n### Individual Assertions\n\n\n```\n$ poetry run netcheck check --type=dns --should-fail\nPassed but was expected to fail.\n{\'type\': \'dns\', \'nameserver\': None, \'host\': \'github.com\', \'A\': [\'20.248.137.48\']}\n```\n\nA few other individual examples:\n```\n./netcheck check --type=dns --server=1.1.1.1 --host=hardbyte.nz --should-fail\n./netcheck check --type=dns --server=1.1.1.1 --host=hardbyte.nz --should-pass\n./netcheck check --type=http --method=get --url=https://s3.ap-southeast-2.amazonaws.com --should-pass\n```\n\nOutput is quiet by default, json available with `--json` (TODO).\n\n\n### Configuration via file\n\nThe main way to run `netcheck` is passing in a list of assertions. \nA json file can be provided with a list of assertions to be checked:\n\n```json\n{\n  "assertions": [\n    {"name":  "deny-cloudflare-dns", "rules": [{"type": "dns", "server":  "1.1.1.1", "host": "github.com", "expected": "pass"}] }\n  ]\n}\n```\n\nAnd the command can be called:\n```\n$ poetry run netcheck run --config config.json \n```\n\n\n## Development\n\nBuild and publish with poetry. First update the version.\n\n```\npoetry version patch\npoetry build\npoetry publish\n```\n',
    'author': 'Brian Thorne',
    'author_email': 'brian@thorne.link',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
