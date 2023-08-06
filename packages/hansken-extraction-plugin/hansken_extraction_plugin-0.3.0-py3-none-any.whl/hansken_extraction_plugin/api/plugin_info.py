"""This module contains all definitions to describe meta data of a plugin, a.k.a. PluginInfo."""
from enum import Enum
from typing import Any

from attr import dataclass


@dataclass
class Author:
    """
    The author of an Extraction Plugin.

    This information can be retrieved by an end-user from Hansken.
    """

    name: str
    email: str
    organisation: str


class MaturityLevel(Enum):
    """This class represents the maturity level of an extraction plugin."""

    PROOF_OF_CONCEPT = 0
    READY_FOR_TEST = 1
    PRODUCTION_READY = 2


@dataclass
class PluginInfo:
    """This information is used by Hansken to identify and run the plugin."""

    plugin: Any  # noqa
    name: str
    version: str
    description: str
    author: Author
    maturity: MaturityLevel
    matcher: str
    webpage_url: str
    deferred_iterations: int = 1
