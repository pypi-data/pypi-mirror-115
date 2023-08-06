import re

from version_helper import Git

SEMVER_PATTERN = r'^(?P<major>0|(?:[1-9]\d*))(?:\.(?P<minor>0|(?:[1-9]\d*))(?:\.(?P<patch>0|(?:[1-9]\d*)))(?:\-(?P<prerelease>[\w\d\.-]+))?(?:\+(?P<build>[\w\d\.-]+))?)?$'
GIT_DESCRIBE_PATTERN = r'^(?P<major>0|(?:[1-9]\d*))(?:\.(?P<minor>0|(?:[1-9]\d*)))(?:\.(?P<patch>0|(?:[1-9]\d*)))(?:\-(?P<prerelease>(?:[\w\d\-]+\.?)+)(?=\-(?:\d+\-[\w\d]{8}(?:\-[\d\w\-]+)?)$))?(?:\-(?P<build>\d+\-[\w\d]{8}(?:\-[\d\w\-]+)?))?$'


class Version:
    """Semantic Versioning compatible class for parsing and emitting SemVer strings into a `Version` object

    More details on Semantic Versioning can be found at https://semver.org/
    """

    def __init__(self, major: int, minor: int, patch: int,
                 prerelease: str = None, build: str = None):
        """Create a `Version` object with the given attributes

        :param major: MAJOR version when you make incompatible API changes
        :param minor: MINOR version when you add functionality in a backwards compatible manner
        :param patch: PATCH version when you make backwards compatible bug fixes
        :param prerelease: Pre-release version string like `alpha.0` or `beta.3`
        :param build: Build metadata
        """
        self.major: int = major
        self.minor: int = minor
        self.patch: int = patch
        self.prerelease: str = prerelease
        self.build: str = build

    def __repr__(self):
        return self.full

    def __str__(self):
        return self.full

    @staticmethod
    def parse(string: str, is_from_git_describe: bool = False) -> 'Version':
        """Parse a version string into it's individual Semantic Versioning parts

        :param string: A Semantic Versioning string
        :param is_from_git_describe: Wether or not the version string is from `git describe`
        :return: A `Version` class object
        """
        pattern = SEMVER_PATTERN
        if is_from_git_describe:
            pattern = GIT_DESCRIBE_PATTERN

        match = None
        if string:
            match = re.fullmatch(pattern, string.strip())

        if match:
            match_dict = match.groupdict()

            return Version(
                major=int(match_dict.get('major')),
                minor=int(match_dict.get('minor')),
                patch=int(match_dict.get('patch')),
                prerelease=match_dict.get('prerelease'),
                build=match_dict.get('build'),
            )
        else:
            raise ValueError('`version_string` is not valid to Semantic Versioning Specification')

    @classmethod
    def get_from_git_describe(cls, dirty=False) -> 'Version':
        """Get a semantic version from git describe

        :param dirty: Append '-dirty' to the build context, if the working tree has local modifications
        :return: A `Version` class object
        """
        description = Git.describe(dirty=dirty)
        return cls.parse(description, True)

    def set(self, major: int, minor: int, patch: int,
            prerelease: str = None, build: str = None):
        """Set `Version` attributes

        :param major: MAJOR version when you make incompatible API changes
        :param minor: MINOR version when you add functionality in a backwards compatible manner
        :param patch: PATCH version when you make backwards compatible bug fixes
        :param prerelease: Pre-release version string like `alpha.0` or `beta.3`
        :param build: Build metadata
        """
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.build = build

    @property
    def core(self) -> str:
        """Core version string including major, minor and patch

        :return: Core version string
        """
        return f'{self.major}.{self.minor}.{self.patch}'

    @property
    def full(self) -> str:
        """Full Semantic Version string including prerelease and build metadata

        :return: Full version string with all it's Semantic Versioning parts
        """
        semver = f'{self.major}.{self.minor}.{self.patch}'
        if self.prerelease:
            semver += f'-{self.prerelease}'
        if self.build:
            semver += f'+{self.build}'
        return semver
