from pydantic import BaseModel

from constants.move_modifier_type import MoveModifierType


class MoveModifier(BaseModel):
    modifier_type: MoveModifierType
    value: float
