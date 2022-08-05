from dataclasses import dataclass, field
from typing import Any


@dataclass
class Slot:
	"""Data-class of a node's slot."""

	id: int
	name: str
	value: Any = field(default=None)
