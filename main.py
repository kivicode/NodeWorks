from nodeworks.presets import ValueNode, SumNode
from nodeworks import Graph


if __name__ == '__main__':
    net = Graph()

    # Leaf nodes
    v1 = net.add_node(ValueNode(1))
    v2 = net.add_node(ValueNode(2))
    v3 = net.add_node(ValueNode(3))

    # Sum nodes
    s1 = net.add_node(SumNode())
    s2 = net.add_node(SumNode())
    s3 = net.add_node(SumNode())

    s21 = net.add_node(SumNode())
    s22 = net.add_node(SumNode())

    # Edges
    net.add_edge(v1, s1, 0, 0)
    net.add_edge(v1, s2, 0, 0)

    net.add_edge(v2, s1, 0, 1)
    net.add_edge(v2, s3, 0, 0)

    net.add_edge(v3, s2, 0, 1)
    net.add_edge(v3, s3, 0, 1)

    # Summation
    net.add_edge(s1, s21, 0, 0)
    net.add_edge(s2, s21, 0, 1)

    net.add_edge(s2, s22, 0, 0)
    net.add_edge(s3, s22, 0, 1)

    out = net.compute_all()
    print(out)

    poss = {
        v1: (0,  0),
        v2: (0, 10),
        v3: (0, 20),

        s1: (30, 0),
        s2: (30, 10),
        s3: (30, 20),

        s21: (60, 5),
        s22: (60, 15),
    }
    net.draw(pos=poss)
