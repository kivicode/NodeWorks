from nodeworks.presets import ValueNode, SumNode
from nodeworks import Graph


if __name__ == '__main__':
    graph = Graph()

    ii = [graph.add_node(SumNode() if i == 1 else ValueNode()) for i in range(5)]
    graph.add_edge(0, 1)
    graph.add_edge(0, 1, 0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(3, 2)
    graph.add_edge(3, 1)
    graph.add_edge(2, 4)
    print(graph.compute(4))
    graph.draw()
