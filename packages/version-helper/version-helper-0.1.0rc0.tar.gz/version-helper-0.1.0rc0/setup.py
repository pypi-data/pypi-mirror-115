# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['version_helper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'version-helper',
    'version': '0.1.0rc0',
    'description': 'Helpers for a better version management in python projects',
    'long_description': '# Version Helper\n\n`version-helper` is a package for a better version management in python projects.\n\n![License?][shield-license]\n\n    from version_helper import Version\n\n    # Parse output from `git describe --tag` and return a semantic versioning compatible `Version` object\n    v = Version.get_from_git_describe()\n\n    # Output core version string including major, minor and patch\n    print(v.core)\n\n    # Output full Semantic Version string including core, prerelease and build metadata\n    print(v.full)\n\n## Table of Contents\n\n- [References](#references)\n\n## Publish\n\n    poetry publish --build [-r testpypi]\n\n## References\n\n- [git-describe](https://git-scm.com/docs/git-describe)\n- [Poetry](https://python-poetry.org/)\n- [Semantic Versioning](https://semver.org/)\n\n\n\n[shield-license]: https://img.shields.io/badge/license-MIT-blue.svg "MIT License"\n',
    'author': 'DL6NM',
    'author_email': 'mail@dl6nm.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dl6nm/version-helper',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
