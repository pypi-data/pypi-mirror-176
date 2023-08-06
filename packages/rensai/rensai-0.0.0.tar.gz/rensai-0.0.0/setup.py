# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rensai']

package_data = \
{'': ['*']}

install_requires = \
['named>=1.1.0']

setup_kwargs = {
    'name': 'rensai',
    'version': '0.0.0',
    'description': 'Serialization framework for Python.',
    'long_description': '# `rensai`\n\n[![License][License Badge]][License]\n[![Version][Version Badge]][Package]\n[![Downloads][Downloads Badge]][Package]\n[![Discord][Discord Badge]][Discord]\n\n[![Documentation][Documentation Badge]][Documentation]\n[![Check][Check Badge]][Actions]\n[![Test][Test Badge]][Actions]\n[![Coverage][Coverage Badge]][Coverage]\n\n> *Serialization framework for Python.*\n\n## Installing\n\n**Python 3.7 or above is required.**\n\n### pip\n\nInstalling the library with `pip` is quite simple:\n\n```console\n$ pip install rensai\n```\n\nAlternatively, the library can be installed from source:\n\n```console\n$ git clone https://github.com/nekitdev/rensai.git\n$ cd rensai\n$ python -m pip install .\n```\n\n### poetry\n\nYou can add `rensai` as a dependency with the following command:\n\n```console\n$ poetry add rensai\n```\n\nOr by directly specifying it in the configuration like so:\n\n```toml\n[tool.poetry.dependencies]\nrensai = "^0.0.0"\n```\n\nAlternatively, you can add it directly from the source:\n\n```toml\n[tool.poetry.dependencies.rensai]\ngit = "https://github.com/nekitdev/rensai.git"\n```\n\n## Examples\n\n<!-- TODO: add examples -->\n\n## Documentation\n\nYou can find the documentation [here][Documentation].\n\n## Support\n\nIf you need support with the library, you can send an [email][Email]\nor refer to the official [Discord server][Discord].\n\n## Changelog\n\nYou can find the changelog [here][Changelog].\n\n## Security Policy\n\nYou can find the Security Policy of `rensai` [here][Security].\n\n## Contributing\n\nIf you are interested in contributing to `rensai`, make sure to take a look at the\n[Contributing Guide][Contributing Guide], as well as the [Code of Conduct][Code of Conduct].\n\n## License\n\n`rensai` is licensed under the MIT License terms. See [License][License] for details.\n\n[Email]: mailto:support@nekit.dev\n\n[Discord]: https://nekit.dev/discord\n\n[Actions]: https://github.com/nekitdev/rensai/actions\n\n[Changelog]: https://github.com/nekitdev/rensai/blob/main/CHANGELOG.md\n[Code of Conduct]: https://github.com/nekitdev/rensai/blob/main/CODE_OF_CONDUCT.md\n[Contributing Guide]: https://github.com/nekitdev/rensai/blob/main/CONTRIBUTING.md\n[Security]: https://github.com/nekitdev/rensai/blob/main/SECURITY.md\n\n[License]: https://github.com/nekitdev/rensai/blob/main/LICENSE\n\n[Package]: https://pypi.org/project/rensai\n[Coverage]: https://codecov.io/gh/nekitdev/rensai\n[Documentation]: https://nekitdev.github.io/rensai\n\n[Discord Badge]: https://img.shields.io/badge/chat-discord-5865f2\n[License Badge]: https://img.shields.io/pypi/l/rensai\n[Version Badge]: https://img.shields.io/pypi/v/rensai\n[Downloads Badge]: https://img.shields.io/pypi/dm/rensai\n\n[Documentation Badge]: https://github.com/nekitdev/rensai/workflows/docs/badge.svg\n[Check Badge]: https://github.com/nekitdev/rensai/workflows/check/badge.svg\n[Test Badge]: https://github.com/nekitdev/rensai/workflows/test/badge.svg\n[Coverage Badge]: https://codecov.io/gh/nekitdev/rensai/branch/main/graph/badge.svg\n',
    'author': 'nekitdev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nekitdev/rensai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
