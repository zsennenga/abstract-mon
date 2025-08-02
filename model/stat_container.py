import math

from pydantic import BaseModel

from constants.stat_stage_multipliers import STAT_STAGE_MULTIPLIERS
from constants.stats import Stat
from model.nature import Nature
from util.stat_stage_util import normalize_stage


def _min_1(value: int) -> int:
    # Pokemon stats never go below 1
    if value < 1:
        return 1
    return value


class StatContainer(BaseModel):
    level: int
    nature: Nature
    base_hp: int
    base_attack: int
    base_defense: int
    base_speed: int
    base_special_attack: int
    base_special_defense: int
    stat_change_stages: dict[Stat, int]

    def _level_stat_value(self, stat: int, nature_multiplier: float) -> int:
        return _min_1(
            math.floor(
                (math.floor((2 * stat * self.level) / 100) + 5) * nature_multiplier
            )
        )

    def get_leveled_stat(self, stat: Stat) -> int:
        if stat == Stat.HP:
            return _min_1(
                math.floor((2 * self.base_hp * self.level) / 100) + self.level + 10
            )
        base_stat_map = {
            Stat.ATTACK: self.base_attack,
            Stat.DEFENSE: self.base_defense,
            Stat.SPECIAL_DEFENSE: self.base_special_defense,
            Stat.SPECIAL_ATTACK: self.base_special_attack,
            Stat.SPEED: self.base_speed,
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
        stat_stage = self.stat_change_stages.get(stat, 0)
        return _min_1(
            math.floor(STAT_STAGE_MULTIPLIERS[stat_stage] * self.get_leveled_stat(stat))
        )

    def get_stat_stage(self, stat: Stat) -> int:
        return normalize_stage(self.stat_change_stages.get(stat, 0))

    def set_stat_stage(self, stat: Stat, stage: int) -> None:
        """
        Explicitly set a stat's stage value.

        Parameters
        ----------
        stat : Stat
            The stat whose stage should be updated.
        stage : int
            The new stage value to set (will be normalized to valid bounds).
        """
        self.stat_change_stages[stat] = normalize_stage(stage)
