from nodeworks.core import BaseNode, Slot


class ValueNode(BaseNode):

	def __init__(self, value: float):
		super().__init__(
			[Slot(0, 'val', value)], [Slot(0, '')]
		)

	def _compute(self):
		return {0: self.input_value(0)}
