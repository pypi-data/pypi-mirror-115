from .version import __version__

# noinspection PyProtectedMember
from ._terality.terality_structures.top_level import (
    _get_top_level_attribute,
    _top_level_functions,
)
from ._terality.terality_structures.dataframe import DataFrame
from ._terality.terality_structures.index import Index
from ._terality.terality_structures.series import Series


def __getattr__(attribute: str):
    return _get_top_level_attribute(attribute)


def __dir__():
    # Static members.
    members = set(name for name in globals() if not name.startswith("_"))
    # Dynamic members.
    members |= _top_level_functions
    return members
