from dataclasses import dataclass, field
from typing import Any


@dataclass
class Slot:
	id: int
	name: str
	value: Any = field(default=None)
