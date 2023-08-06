import pathlib
from enum import Enum


PROFILE_FILENAME = ".neosctl"
PROFILE_FILEPATH = pathlib.Path().home() / PROFILE_FILENAME


DEFAULT_PROFILE = "default"


class AuthFlow(Enum):
    keycloak = "keycloak"
