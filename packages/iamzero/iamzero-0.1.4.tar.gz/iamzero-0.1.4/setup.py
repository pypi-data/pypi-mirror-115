# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iamzero', 'iamzero.instrumentation']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'statsd>=3.3.0,<4.0.0', 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'iamzero',
    'version': '0.1.4',
    'description': 'iam-zero least-privilege instrumentation client for Python',
    'long_description': '<p align="center"><img src="https://iamzero.dev/img/logo-boxed.svg" height="80" /></p>\n\n<h1 align="center">iamzero-python</h1>\n<p align="center">Python client library for <a href="https://iamzero.dev">IAM Zero</a></p>\n\n<p align="center">\n<a align="center" href="https://twitter.com/intent/tweet?url=https%3A%2F%2Fiamzero.dev&text=IAM%20Zero%20simplifies%20cloud%20permissions%20for%20development%20teams"><img src="https://img.shields.io/twitter/url/https/github.com/tterb/hyde.svg?style=social" alt="tweet" /></a>\n<a href="https://join.slack.com/t/commonfatecommunity/shared_invite/zt-q4m96ypu-_gYlRWD3k5rIsaSsqP7QMg"><img src="https://img.shields.io/badge/slack-iamzero-1F72FE.svg?logo=slack" alt="slack" /></a>\n</p>\n\n<p align="center">\n    <a href="https://iamzero.dev/docs/getting-started">🚀 Get Started</a> |\n    <a href="https://iamzero.dev/docs/support">📖 Support</a>\n</p>\n\nThis package makes it easy to create least-privilege IAM policies for your Python scripts or applications.\n\n## What is IAM Zero?\n\nIAM Zero detects identity and access management issues and automatically suggests least-privilege policies. It does this by capturing errors in applications you build or commands that you run which use. By detecting the error and matching it against our Access Advisory lists IAM Zero can instantly provide a least-privilege policy recommendation, customised to your cloud environment.\n\nIAM Zero currently works for AWS but our roadmap includes other cloud platforms like GCP, Azure, and Kubernetes.\n\n## Documentation\n\nGet started by [reading our documentation](https://iamzero.dev/docs/getting-started).\n\n## Contributing\n\nSee [CONTRIBUTING.md](./CONTRIBUTING.md) for information on how to contribute. We welcome all contributors - [join our Slack](https://join.slack.com/t/commonfatecommunity/shared_invite/zt-q4m96ypu-_gYlRWD3k5rIsaSsqP7QMg) to discuss the project!\n\n## Security\n\nYou can view our full security documentation on the [IAM Zero website](https://iamzero.dev/docs/security).\n',
    'author': 'Common Fate',
    'author_email': 'hello@commonfate.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://iamzero.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
