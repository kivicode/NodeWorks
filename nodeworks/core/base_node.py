from typing import Collection, Any, Dict
from abc import abstractmethod, ABC

from nodeworks.core.slot import Slot
from nodeworks.utils.hints import overridable


class BaseNode(ABC):

	def __init__(self, in_slots: Collection[Slot] = tuple(), out_slots: Collection[Slot] = tuple()):
		self.index = None
		self._in_slots = in_slots
		self._out_slots = out_slots

	@property
	def inputs(self) -> Collection[Slot]:
		return self._in_slots

	def input_value(self, slot_index: int) -> Any:
		return self._in_slots[slot_index].value

	@property
	def outputs(self) -> Collection[Slot]:
		return self._out_slots

	def set_input(self, slot_index: int, value) -> None:
		if not self.verify_input(slot_index, value):
			raise ValueError(f"Incorrect input type for slot {slot_index}: {type(value)}")

		new_value = self.on_set_input(slot_index, value)
		self._in_slots[slot_index].value = new_value if new_value is not None else value

	def set_output(self, slot_index: int, value) -> None:
		self.outputs[slot_index].value = value

	@overridable
	def verify_input(self, slot_index: int, value) -> bool:
		return True

	@overridable
	def on_set_input(self, slot_index: int, value) -> Any:
		...

	def forward(self):
		outputs = self._compute()
		for k, v in outputs.items():
			self._out_slots[k].value = v
		return [s.value for s in self._out_slots]

	@abstractmethod
	def _compute(self) -> Dict[int, Any]:
		...

	def has_slot(self, slot_index: int, search_output: bool = False) -> bool:
		pool = self.outputs if search_output else self.inputs
		return slot_index in map(lambda s: s.id, pool)
