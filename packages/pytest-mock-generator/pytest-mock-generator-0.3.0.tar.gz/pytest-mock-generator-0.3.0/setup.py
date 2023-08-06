# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_mock_generator']

package_data = \
{'': ['*']}

install_requires = \
['mock-generator>=2.2.1,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.5.0,<5.0.0']}

entry_points = \
{'pytest11': ['pytest_mock_generator = pytest_mock_generator']}

setup_kwargs = {
    'name': 'pytest-mock-generator',
    'version': '0.3.0',
    'description': 'A pytest fixture wrapper for https://pypi.org/project/mock-generator',
    'long_description': '# pytest-mock-generator\n\n<div align="center">\n\n[![Build status](https://github.com/pksol/pytest-mock-generator/workflows/build/badge.svg?branch=master&event=push)](https://github.com/pksol/pytest-mock-generator/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/pytest-mock-generator.svg)](https://pypi.org/project/pytest-mock-generator/)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pksol/pytest-mock-generator/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/pksol/pytest-mock-generator/releases)\n[![License](https://img.shields.io/github/license/pksol/pytest-mock-generator)](https://github.com/pksol/pytest-mock-generator/blob/master/LICENSE)\n\nA pytest fixture wrapper for https://pypi.org/project/mock-generator\n\n</div>\n\n## Installation\n\n```bash\npip install pytest-mock-generator\n```\n\nor install with `Poetry`\n\n```bash\npoetry add pytest-mock-generator\n```\n\n\n## 📈 Releases\n\nYou can see the list of available releases on the [GitHub Releases](https://github.com/pksol/pytest-mock-generator/releases) page.\n\nWe follow [Semantic Versions](https://semver.org/) specification.\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/pksol/pytest-mock-generator)](https://github.com/pksol/pytest-mock-generator/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/pksol/pytest-mock-generator/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```bibtex\n@misc{pytest-mock-generator,\n  author = {Peter Kogan},\n  title = {A pytest fixture wrapper for https://pypi.org/project/mock-generator},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/pksol/pytest-mock-generator}}\n}\n```\n\n## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)\n',
    'author': 'Peter Kogan',
    'author_email': 'kogan.peter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pksol/pytest-mock-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
