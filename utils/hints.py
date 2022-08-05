from collections import defaultdict
from typing import Callable, TypeVar

_OVERRIDABLE_METHODS_MAP = defaultdict(list)


def overridable(method: Callable):
	_OVERRIDABLE_METHODS_MAP[method.__qualname__].append(method.__name__)
	return method


def get_overridable_fields(cls: TypeVar):
	keys = filter(lambda m: m.startswith(cls.__name__ + '.'), _OVERRIDABLE_METHODS_MAP)
	return [_OVERRIDABLE_METHODS_MAP[k] for k in keys]
