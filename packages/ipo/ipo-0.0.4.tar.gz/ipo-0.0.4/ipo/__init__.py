#!/usr/bin/env python3

# © 2020-2021, Midgard
# License: LGPL-3.0-or-later

# pylint: disable=invalid-name

import sys
import io
import csv
import itertools
import re
from functools import wraps
from typing import \
	overload, cast, TypeVar, Union, Any, AnyStr, Iterable, Iterator, Callable, Tuple, Sequence, \
	List, Optional, Mapping, Dict, Literal, Match, Generic


_T = TypeVar("_T")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")
_T4 = TypeVar("_T4")
_T5 = TypeVar("_T5")
_T6 = TypeVar("_T6")
_T7 = TypeVar("_T7")
_T8 = TypeVar("_T8")
_T9 = TypeVar("_T9")
_U = TypeVar("_U")
_U2 = TypeVar("_U2")


class ipo(Generic[_T]):
	def __init__(self, data: _T) -> None:
		self.data = data

	# Make it possible to pipe, e.g.
	#   ipo([1, 5, 3]) | sorted
	def __or__(self, function: Callable[[_T], _U]) -> "ipo[_U]":
		return ipo(function(self.data))

	def __eq__(self, other: Any) -> bool:
		return other.__class__ == ipo and self.data == other.data

	def __repr__(self) -> str:
		return "ipo({0!r})".format(self.data)


@overload
def ipo_source(function: Callable[[                                          ], _U]) -> Callable[[                                          ], ipo[_U]]: ...
@overload
def ipo_source(function: Callable[[_T                                        ], _U]) -> Callable[[_T                                        ], ipo[_U]]: ...
@overload
def ipo_source(function: Callable[[_T, _T2                                   ], _U]) -> Callable[[_T, _T2                                   ], ipo[_U]]: ...
@overload
def ipo_source(function: Callable[[_T, _T2, _T3                              ], _U]) -> Callable[[_T, _T2, _T3                              ], ipo[_U]]: ...
@overload
def ipo_source(function: Callable[[_T, _T2, _T3, _T4                         ], _U]) -> Callable[[_T, _T2, _T3, _T4                         ], ipo[_U]]: ...
@overload
def ipo_source(function: Callable[[_T, _T2, _T3, _T4, _T5                    ], _U]) -> Callable[[_T, _T2, _T3, _T4, _T5                    ], ipo[_U]]: ...
@overload
def ipo_source(function: Callable[[_T, _T2, _T3, _T4, _T5, _T6               ], _U]) -> Callable[[_T, _T2, _T3, _T4, _T5, _T6               ], ipo[_U]]: ...
@overload
def ipo_source(function: Callable[[_T, _T2, _T3, _T4, _T5, _T6, _T7          ], _U]) -> Callable[[_T, _T2, _T3, _T4, _T5, _T6, _T7          ], ipo[_U]]: ...
@overload
def ipo_source(function: Callable[[_T, _T2, _T3, _T4, _T5, _T6, _T7, _T8     ], _U]) -> Callable[[_T, _T2, _T3, _T4, _T5, _T6, _T7, _T8     ], ipo[_U]]: ...
@overload
def ipo_source(function: Callable[[_T, _T2, _T3, _T4, _T5, _T6, _T7, _T8, _T9], _U]) -> Callable[[_T, _T2, _T3, _T4, _T5, _T6, _T7, _T8, _T9], ipo[_U]]: ...

def ipo_source(function):
	"""
	Decorator for functions that should return ipo data.
	"""
	@wraps(function)
	def f(*args, **kwargs):
		return ipo(function(*args, **kwargs))
	return f


# =================================================================================
# STANDARD LIBRARY

# ----------------------------------------------------
# I/O


# This must not be decorated with @ipo because it has to generate data.
@ipo_source
def read(file):
	return (line.rstrip("\n") for line in file)

stdin = read(sys.stdin)


def write(str_or_iter: Any, **kwargs) -> None:
	"""
	Write to file. If the data is iterable, each item is printed on its own line.

	Exception: strings and bytes are not iterated but printed as-is.
	"""
	if isinstance(str_or_iter, (str, bytes)):
		print(str_or_iter, **kwargs)
		return

	try:
		it = iter(str_or_iter)
	except TypeError:
		print(str_or_iter, **kwargs)
		return

	for x in it:
		print(x, **kwargs)


# ----------------------------------------------------
# CSV

from_csv = csv.reader


def to_csv(
		data: Iterable[Any], separator: str=",", quotechar: str='"', escapechar: Optional[str]=None,
		quoteall: bool=False
) -> Iterable[str]:
	# We have our own CSV writer because csv.writer insists upon writing to a file

	if escapechar is None:
		escapechar = quotechar

	def serialize(item):
		if item is None:
			return ""

		item_s = str(item)

		# If item should not be quoted
		if not quoteall and quotechar not in item_s and "\n" not in item_s:
			return item_s

		if quotechar != escapechar:
			item_s = item_s.replace(escapechar, escapechar + escapechar)
		item_s = item_s.replace(quotechar, escapechar + quotechar)
		return quotechar + item_s + quotechar

	return (
		separator.join(serialize(item) for item in line)
		for line in data
	)


@overload
def recompose(
	selection: Iterable[Callable[[_T], _U]],
	data: Iterable[_T]
) -> Tuple[_U]:
	...
@overload
def recompose(
	selection: Iterable[Union[Callable[[_T], _T], int]],
	data: Sequence[_T]
) -> Tuple[_T]:
	...

def recompose(selection: Iterable[Union[Callable[[Any], Any], Any]], data: Any) -> Sequence[Any]:
	"""
	`selection` is an iterable where each item specifies a field in the resulting tuple:
	- a callable is called on `data`, the result is taken,
	- another element is used as an index in `data`.

	This is especially useful in conjunction with `map`, e.g. to transform tabular data.

	If ints are used, `data` should support indexing (so a list or tuple is fine,
	but a generator is not).

	>>> from functools import partial as p
	>>> (
	...   ipo([(3, 4, 5), ("a", "b")]) |
	...   p(map, p(recompose,
	...     [0, lambda x: x[0] + x[1]]
	...   )) | list
	... )
	ipo([(3, 7), ("a", "ab")])
	"""
	return tuple(
		(sel(data) if callable(sel) else data[sel])
		for sel in selection
	)


# ----------------------------------------------------
# Iterable stuff


def starstarmap(function: Callable[..., _T], data: Iterable[Any], *args: Iterable[Any]) \
		-> Iterator[_T]:
	return map(lambda x: function(*args, **x), data)


flatten = itertools.chain.from_iterable

# Some aliases for common usages of slicing makes things more understandable
def head(n: int, data: Iterable[_T]) -> Iterator[_T]:
	return itertools.islice(data, n)
def skip(n: int, data: Iterable[_T]) -> Iterator[_T]:
	return itertools.islice(data, n, None)


def prepended(data_to_prepend: Iterable[_T], data: Iterable[_T]) -> Iterator[_T]:
	return itertools.chain(data_to_prepend, data)


def appended(data_to_append: Iterable[_T], data: Iterable[_T]) -> Iterator[_T]:
	return itertools.chain(data, data_to_append)


def parted(predicate_or_amount: Union[int, Callable[[_T, int], bool]], data: Iterable[_T]) \
		-> Tuple[List[_T], Optional[Iterator[_T]]]:
	"""
	Two parts of data, delimited by the first element for which the predicate is truthy.

	If a delimiter is found, the second part is an iterator over the remaining elements.
	Else it is None.
	"""
	first = []

	predicate = (lambda item, index: index == predicate_or_amount) \
		if isinstance(predicate_or_amount, int) else \
		predicate_or_amount

	it = iter(data)
	index = 0
	try:
		item = next(it)
		while not predicate(item, index):
			first.append(item)
			item = next(it)
			index += 1
	except StopIteration:
		return (first, None)

	return (first, itertools.chain((item,), it))


def all_before(predicate: Callable[[_T], Any], data: Iterable[_T]) -> Iterable[_T]:
	for item in data:
		if predicate(item):
			return
		yield item


def all_after(predicate: Callable[[_T], Any], data: Iterable[_T]) -> Iterable[_T]:
	it = iter(data)
	for item in it:
		if predicate(item):
			yield item
			yield from it
			return


def flat_enum(data: Iterable[Any], start: int=0) -> Iterable[Tuple[int, ...]]:
	return (
		(i, *els)
		for i, els in enumerate(data, start=start)
	)


def intersperse(separator: _T, data: Iterable[_T2]) -> Iterable[Union[_T, _T2]]:
	it = iter(data)

	# Yield first element
	try:
		yield next(it)
	except StopIteration:
		return

	# Yield remaining elements per pair of (separator, element)
	yield from itertools.chain.from_iterable(
		cast( # We need a cast() because zip() returns a "zip object" that makes the type checker trip
			Iterable[Iterable[Union[_T, _T2]]],
			zip(itertools.repeat(separator), it)
		)
	)


# ----------------------------------------------------
# Dict stuff

def dictmap(function: Callable[[_T, _T2], Tuple[_U, _U2]], data: Mapping[_T, _T2]) -> Dict[_U, _U2]:
	return dict(
		function(k, v)
		for k, v in data.items()
	)


# ----------------------------------------------------
# Shell-like utils

def grep(pattern: AnyStr, data: Iterable[AnyStr], flags: int=0) -> Iterable[AnyStr]:
	"""
	Like grep -E or egrep
	"""
	return (
		item
		for item in data
		if re.search(pattern, item, flags)
	)


@overload
def grepo(pattern: AnyStr, data: Iterable[AnyStr], match_objects: Literal[False], flags: int) \
		-> Iterable[AnyStr]: ...
@overload
def grepo(pattern: AnyStr, data: Iterable[AnyStr], match_objects: Literal[True], flags: int) \
		-> Iterable[Match[AnyStr]]: ...

def grepo(pattern, data, match_objects=False, flags=0):
	"""
	Like grep -E -o (keep only the matched parts, with each such part in a separate output item)

	:param match_objects: False to return strings, True to return tuples of match objects
	"""
	if match_objects:
		for item in data:
			yield from re.finditer(pattern, item, flags)
	else:
		for item in data:
			yield from (
				match.group(0)
				for match in re.finditer(pattern, item, flags)
			)
