# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Releases]

_All releases will be published to [PyPI]._

### [0.1.2] (2021-08-10)

#### Fixed

- Fix error in workflow on uploading coverage report to Codecov

### [0.1.1] (2021-08-10)

#### Added

- Add GitHub workflow for running tests and getting the code coverage with [Codecov](https://app.codecov.io/gh/dl6nm/version-helper)
- Add [CHANGELOG.md](CHANGELOG.md)

### [0.1.0] (2021-08-09)

#### Added

- Add tests and fixtures for `Git` class and its methods
- Implement `Git` class with method...
  - `exec_path()` for getting the installation path of git
  - `describe()` to get a human-readable string containing the most recent tag
- Implement `Version.get_from_git_describe()` to get a `Version` object from a `git describe` call
- Add code examples to [README.md](README.md)


### [0.0.1] (2021-07-30)

#### Added

- Add tests and fixtures for `Version` class and its methods
- Implement `Version` class with method...
  - `parser()` for converting a string into a [Semantic Versioning] like `Version` object
  - `set()` for setting or changing a version explicitly
- Add [README.md](README.md)



[0.1.2]: https://github.com/dl6nm/version-helper/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/dl6nm/version-helper/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/dl6nm/version-helper/compare/0.0.1...0.1.0
[0.0.1]: https://github.com/dl6nm/version-helper/releases/tag/0.0.1

[releases]: https://github.com/dl6nm/version-helper/
[pypi]: https://pypi.org/project/version-helper/

[Keep a Changelog]: https://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html