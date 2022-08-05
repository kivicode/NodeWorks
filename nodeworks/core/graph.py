from typing import Dict, Optional

import networkx as nx
import matplotlib.pyplot as plt

from .edge import Edge
from .base_node import BaseNode
from .errors import NodeError


class Graph:

	def __init__(self, **attrs):
		self._attrs = attrs
		self._graph = nx.MultiDiGraph(incoming_graph_data=None)
		self._nodes: Dict[int, BaseNode] = {}

	def add_node(self, node: BaseNode) -> int:
		node.index = index = len(self._graph)
		self._nodes[index] = node
		self._graph.add_node(index)
		return index

	def add_edge(self, from_id: int, to_id: int, from_slot: int = 0, to_slot: int = 0):
		if not self._nodes[from_id].has_slot(from_slot, True):
			raise NodeError(f"No outgoing slot '{from_slot}' found for the source node {self._nodes[from_id]}")

		if not self._nodes[to_id].has_slot(to_slot):
			raise NodeError(f"No incoming slot '{to_slot}' found for the target node {self._nodes[to_id]}")

		edge = Edge(from_id, from_slot, to_id, to_slot)
		self._graph.add_edge(from_id, to_id, key=edge)

	def compute(self, end_node: int):
		path = nx.edge_bfs(self._graph, end_node, 'reverse')

		for e_from, e_to, edge, _ in list(path)[::-1]:
			start, end = self._nodes[edge.from_node], self._nodes[edge.to_node]
			out = start.forward()
			end.set_input(edge.to_slot, out[edge.from_slot])
		return self._nodes[end_node].forward()

	def draw(self, **kwargs):
		nx.draw(self._graph, with_labels=True, **kwargs)
		plt.show()
