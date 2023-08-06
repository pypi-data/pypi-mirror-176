# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solus']

package_data = \
{'': ['*']}

install_requires = \
['named>=1.1.0']

setup_kwargs = {
    'name': 'solus',
    'version': '1.1.0',
    'description': 'Singleton types.',
    'long_description': '# `solus`\n\n[![License][License Badge]][License]\n[![Version][Version Badge]][Package]\n[![Downloads][Downloads Badge]][Package]\n[![Discord][Discord Badge]][Discord]\n\n[![Documentation][Documentation Badge]][Documentation]\n[![Check][Check Badge]][Actions]\n[![Test][Test Badge]][Actions]\n[![Coverage][Coverage Badge]][Coverage]\n\n> *Singleton types.*\n\n## Installing\n\n**Python 3.7 or above is required.**\n\n### pip\n\nInstalling the library with `pip` is quite simple:\n\n```console\n$ pip install solus\n```\n\nAlternatively, the library can be installed from source:\n\n```console\n$ git clone https://github.com/nekitdev/solus.git\n$ cd solus\n$ python -m pip install .\n```\n\n### poetry\n\nYou can add `solus` as a dependency with the following command:\n\n```console\n$ poetry add solus\n```\n\nOr by directly specifying it in the configuration like so:\n\n```toml\n[tool.poetry.dependencies]\nsolus = "^1.1.0"\n```\n\nAlternatively, you can add it directly from the source:\n\n```toml\n[tool.poetry.dependencies.solus]\ngit = "https://github.com/nekitdev/solus.git"\n```\n\n## Examples\n\n### Default\n\n[`Singleton`][solus.core.Singleton] type is used to create *thread-safe* singletons.\n\n```python\nfrom solus import Singleton\n\n\nclass Null(Singleton):\n    ...\n```\n\nSomewhere else in the code:\n\n```python\nnull = Null()  # instantiate\n```\n\n### Unsafe\n\n[`UnsafeSingleton`][solus.core.UnsafeSingleton] type is used to create *thread-unsafe* singletons.\n\n```python\nfrom solus import UnsafeSingleton\n\n\nclass Null(UnsafeSingleton):\n    ...\n\n\nnull = Null()  # instantiate right away\n```\n\n### Warning\n\n!!! warning\n\n    It is highly recommended to instantiate unsafe singleton types right after their creation!\n\n## Documentation\n\nYou can find the documentation [here][Documentation].\n\n## Support\n\nIf you need support with the library, you can send an [email][Email]\nor refer to the official [Discord server][Discord].\n\n## Changelog\n\nYou can find the changelog [here][Changelog].\n\n## Security Policy\n\nYou can find the Security Policy of `solus` [here][Security].\n\n## Contributing\n\nIf you are interested in contributing to `solus`, make sure to take a look at the\n[Contributing Guide][Contributing Guide], as well as the [Code of Conduct][Code of Conduct].\n\n## License\n\n`solus` is licensed under the MIT License terms. See [License][License] for details.\n\n[Email]: mailto:support@nekit.dev\n\n[Discord]: https://nekit.dev/discord\n\n[Actions]: https://github.com/nekitdev/solus/actions\n\n[Changelog]: https://github.com/nekitdev/solus/blob/main/CHANGELOG.md\n[Code of Conduct]: https://github.com/nekitdev/solus/blob/main/CODE_OF_CONDUCT.md\n[Contributing Guide]: https://github.com/nekitdev/solus/blob/main/CONTRIBUTING.md\n[Security]: https://github.com/nekitdev/solus/blob/main/SECURITY.md\n\n[License]: https://github.com/nekitdev/solus/blob/main/LICENSE\n\n[Package]: https://pypi.org/project/solus\n[Coverage]: https://codecov.io/gh/nekitdev/solus\n[Documentation]: https://nekitdev.github.io/solus\n\n[Discord Badge]: https://img.shields.io/badge/chat-discord-5865f2\n[License Badge]: https://img.shields.io/pypi/l/solus\n[Version Badge]: https://img.shields.io/pypi/v/solus\n[Downloads Badge]: https://img.shields.io/pypi/dm/solus\n\n[Documentation Badge]: https://github.com/nekitdev/solus/workflows/docs/badge.svg\n[Check Badge]: https://github.com/nekitdev/solus/workflows/check/badge.svg\n[Test Badge]: https://github.com/nekitdev/solus/workflows/test/badge.svg\n[Coverage Badge]: https://codecov.io/gh/nekitdev/solus/branch/main/graph/badge.svg\n\n[solus.core.Singleton]: https://nekitdev.github.io/solus/reference#solus.Singleton\n[solus.core.UnsafeSingleton]: https://nekitdev.github.io/solus/reference#solus.UnsafeSingleton\n',
    'author': 'nekitdev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nekitdev/solus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
