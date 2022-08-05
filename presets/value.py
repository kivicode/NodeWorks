from core import Node, Slot


class ValueNode(Node):

	def __init__(self):
		super().__init__(
			[Slot(0, 'val', 99)], [Slot(0, '')]
		)

	def _compute(self):
		return {0: self.input_value(0)}
