from nodeworks.core import BaseNode, Slot


class SumNode(BaseNode):

	def __init__(self):
		super().__init__(
			[Slot(0, 'a'), Slot(1, 'b')], [Slot(0, 'sum')]
		)

	def _compute(self):
		return {0: self.input_value(0) + self.input_value(1)}
