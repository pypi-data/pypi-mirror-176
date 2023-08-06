from typing import NamedTuple

from typing_extensions import Final, Literal

__all__ = (
    "__title__",
    "__author__",
    "__license__",
    "__version__",
    "version_info",
)


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]


__title__: Final = "steam"
__author__: Final = "Gobot1234"
__license__: Final = "MIT"
__version__: Final = "1.0.0a1+g1c4f422"
version_info: Final = VersionInfo(major=1, minor=0, micro=0, releaselevel="alpha")
