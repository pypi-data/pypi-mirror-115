"""Utility functions."""

from __future__ import annotations

from functools import reduce
from typing import Any, Mapping, TypeVar, Union, overload

try:
    from typing import Literal  # type: ignore
except ImportError:
    from typing_extensions import Literal  # type: ignore

T = TypeVar("T")
S = TypeVar("S")


def deep_get(data: Mapping[str, Any], key: str, default: Any = None) -> Any:
    """Get deep key."""

    return reduce(lambda x, y: x.get(y, default), key.split("."), data)


@overload
def coalesce(x: Literal[None], y: S) -> S:
    ...


@overload
def coalesce(x: T, y: S) -> T:
    ...


def coalesce(x: T, y: S) -> Union[S, T]:
    """Coalesce values."""

    return x if x is not None else y
