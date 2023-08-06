# Version Helper

`version-helper` is a package for a better version management in python projects.

![License?][shield-license]

    from version_helper import Version

    # Parse output from `git describe --tag` and return a semantic versioning compatible `Version` object
    v = Version.get_from_git_describe()

    # Output core version string including major, minor and patch
    print(v.core)

    # Output full Semantic Version string including core, prerelease and build metadata
    print(v.full)

## Table of Contents

- [References](#references)

## Publish

    poetry publish --build [-r testpypi]

## References

- [git-describe](https://git-scm.com/docs/git-describe)
- [Poetry](https://python-poetry.org/)
- [Semantic Versioning](https://semver.org/)



[shield-license]: https://img.shields.io/badge/license-MIT-blue.svg "MIT License"
