from typing import Collection, Any, Dict, List
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
		"""The list of input slots."""
		return self._in_slots

	def input_value(self, slot_index: int) -> Any:
		"""Helper method for retrieving value of an input slot specified."""
		return self._in_slots[slot_index].value

	@property
	def outputs(self) -> Collection[Slot]:
		"""The list of output slots."""
		return self._out_slots

	def set_input(self, slot_index: int, value) -> None:
		"""Overrides the current input slot's value with a new one.

		Additionally performs a validity check by calling ``self.verify_input(...)``.
		Invokes ``self.on_set_input(...)`` callback and uses its return value (if not None) to set the input.

		Args:
			slot_index: Index of the input slot to write the value to.
			value: New value to override with.

		Raises:
			ValueError: if self.verify_input(...) returned False
		"""
		if not self.verify_input(slot_index, value):
			raise ValueError(f"Incorrect input type for slot {slot_index}: {type(value)}")

		new_value = self.on_set_input(slot_index, value)
		self._in_slots[slot_index].value = new_value if new_value is not None else value

	def set_output(self, slot_index: int, value) -> None:
		"""Helper method for direct setting value of an output slot."""
		self.outputs[slot_index].value = value

	@overridable
	def verify_input(self, slot_index: int, value) -> bool:
		"""User-overridable method to perform a custom check of the incoming data.

		Should return True is everything's ok and False otherwise.
		Always returns True by default.
		"""
		return True

	@overridable
	def on_set_input(self, slot_index: int, value) -> Any:
		"""User-overridable callback invoked by ``self.set_input(...)``.

		Called before setting a new value to an input and can override the new value by returning a non-None value.
		"""
		return None

	def forward(self) -> List[Any]:
		"""Calculates and updates the output value based on the inputs.

		Returns:
			List of output values for all the output slots.
		"""
		outputs = self._compute()
		for k, v in outputs.items():
			self._out_slots[k].value = v
		return [s.value for s in self._out_slots]

	@abstractmethod
	def _compute(self) -> Dict[int, Any]:
		"""Calculates the updated values of the outputs based on the inputs.

		Returns:
			Dict of form {out_slot_id -> new_value}. Returns only updated values.
		"""

	def has_slot(self, slot_index: int, search_output: bool = False) -> bool:
		pool = self.outputs if search_output else self.inputs
		return slot_index in map(lambda s: s.id, pool)

	def __str__(self):
		return f'{self.__class__.__name__}(index={self.index}, in={self.inputs}, out={self.outputs})'

	def __repr__(self):
		return str(self)
