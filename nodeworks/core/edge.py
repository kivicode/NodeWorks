from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Edge:
	"""Data of a graph edge/connection."""

	from_node: int
	from_slot: int

	to_node: int
	to_slot: int
