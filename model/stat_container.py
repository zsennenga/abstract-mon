import math

from pydantic import BaseModel

from constants.stat_stage_multipliers import STAT_STAGE_MULTIPLIERS
from constants.stats import Stat
from model.nature import Nature


class StatContainer(BaseModel):
    level: int
    nature: Nature
    _base_hp: int
    _base_attack: int
    _base_defense: int
    _base_speed: int
    _base_special_attack: int
    _base_special_defense: int
    _stat_change_stages: dict[Stat, int]

    def _level_stat_value(self, stat: int, nature_multiplier: float) -> int:
        return math.floor(
            (math.floor((2 * stat * self.level) / 100) + 5) * nature_multiplier
        )

    def get_leveled_stat(self, stat: Stat) -> int:
        if stat == Stat.HP:
            return math.floor((2 * self._base_hp * self.level) / 100) + self.level + 10
        base_stat_map = {
            Stat.ATTACK: self._base_attack,
            Stat.DEFENSE: self._base_defense,
            Stat.SPECIAL_DEFENSE: self._base_special_defense,
            Stat.SPECIAL_ATTACK: self._base_special_attack,
            Stat.SPEED: self._base_speed,
        }
        if stat not in base_stat_map:
            raise ValueError(f"Cannot get leveled stat for {stat}")
        return self._level_stat_value(
            base_stat_map[stat],
            self.nature.stat_modifiers.get(stat, 1),
        )

    def get_modified_stat(self, stat: Stat) -> int:
        if stat == Stat.HP:
            return self.get_leveled_stat(Stat.HP)
        stat_stage = self._stat_change_stages.get(stat, 1)
        return math.floor(
            STAT_STAGE_MULTIPLIERS[stat_stage] * self.get_leveled_stat(stat)
        )

    def get_stat_stage(self, stat: Stat) -> int:
        return self._stat_change_stages.get(stat, 1)
