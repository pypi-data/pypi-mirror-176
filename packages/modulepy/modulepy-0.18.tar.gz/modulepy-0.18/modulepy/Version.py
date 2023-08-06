from dataclasses import dataclass


@dataclass
class Version:
    major: int
    minor: int
    patch: int

    def __init__(self, major: int = 1, minor: int = 0, patch: int = 0):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch
