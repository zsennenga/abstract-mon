from pydantic import BaseModel

from constants.move_modifier_type import MoveModifierType
from constants.stats import Stat


class MoveMagnitudeModifier(BaseModel):
    modifier_type: MoveModifierType
    value: float


class StatModifier(BaseModel):
    stat: Stat
    stages: int


AnyModifier = StatModifier | MoveMagnitudeModifier


class ModifierContainer(BaseModel):
    round_modifier: list[AnyModifier] = []
    turn_modifier: list[AnyModifier] = []

    @property
    def current_modifiers(self) -> list[AnyModifier]:
        return self.round_modifier + self.turn_modifier

    def get_stat_stage(self, stat: Stat) -> int:
        total_stages = 0
        for modifier in self.current_modifiers:
            if isinstance(modifier, StatModifier) and modifier.stat == stat:
                total_stages += modifier.stages

        return total_stages

    def get_move_modifier(self, modifier_type: MoveModifierType) -> float:
        total_mod = 1.0
        for modifier in self.current_modifiers:
            if isinstance(modifier, MoveMagnitudeModifier):
                if modifier.modifier_type == modifier_type:
                    total_mod *= modifier.value
        return total_mod
