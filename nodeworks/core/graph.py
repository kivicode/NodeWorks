from typing import Dict, Optional, List, Any

import networkx as nx
import matplotlib.pyplot as plt

from .edge import Edge
from .base_node import BaseNode
from .errors import NodeError


class Graph:
	"""Represents a single directional multi-graph of nodes.

	Responsible for constructing, managing and computing of the graph.
	"""

	def __init__(self, **attrs):
		self._attrs = attrs
		self._graph = nx.MultiDiGraph(incoming_graph_data=None)
		self._nodes: Dict[int, BaseNode] = {}

	def add_node(self, node: BaseNode) -> int:
		"""Adds a new node to the graph.

		Args:
			node: Node to be added. Expected to be inherited from the BaseNode.

		Returns:
			Index assigned to the new node.
		"""

		node.index = index = len(self._graph)
		self._nodes[index] = node
		self._graph.add_node(index)
		return index

	def add_edge(self, from_id: int, to_id: int, from_slot: int = 0, to_slot: int = 0) -> None:
		"""Creates a new edge between two slots.

		Performs a check if the target slots are present provided by the nodes.

		Args:
			from_id: Index of the source (emitting) node.
			to_id: Index of the target (receiving) node.
			from_slot: Index of the output slot of the source node.
			to_slot: Index of the input slot of the target node.

		Raises:
			NodeError if failed to find the requested input/output slot.
		"""
		if not self._nodes[from_id].has_slot(from_slot, True):
			raise NodeError(f"No outgoing slot '{from_slot}' found for the source node {self._nodes[from_id]}")

		if not self._nodes[to_id].has_slot(to_slot):
			raise NodeError(f"No incoming slot '{to_slot}' found for the target node {self._nodes[to_id]}")

		edge = Edge(from_id, from_slot, to_id, to_slot)
		self._graph.add_edge(from_id, to_id, key=edge)

	def compute(self, end_node: int) -> List[Any]:
		"""Performs a forward pass from the node provided.

		Uses Breadth-First-Search algorithm to traverse the edges.

		Args:
			end_node: Index of the root node for witch to perform the pass.

		Returns:
			A list of output values of the root (end) node calculated.
		"""
		path = nx.edge_bfs(self._graph, end_node, 'reverse')

		for e_from, e_to, edge, _ in list(path)[::-1]:
			start, end = self._nodes[edge.from_node], self._nodes[edge.to_node]
			out = start.forward()
			end.set_input(edge.to_slot, out[edge.from_slot])
		return self._nodes[end_node].forward()

	def compute_all(self) -> Dict[BaseNode, List[Any]]:
		"""Finds all the root nodes and computes the forward passes for each of them.

		Returns:
			Dictionary of form {root_node_index -> computed outputs}
		"""
		# TODO: Avoid calculating same edge multiple times
		outputs = {}
		for end_node in self.find_end_nodes():
			outputs[self._nodes[end_node]] = self.compute(end_node)
		return outputs

	def find_end_nodes(self) -> List[int]:
		"""Find indices of all the root nodes."""
		return [u for u, deg in self._graph.out_degree if deg == 0]

	def draw(self, **kwargs):
		nx.draw(self._graph, with_labels=True, **kwargs)
		plt.show()
