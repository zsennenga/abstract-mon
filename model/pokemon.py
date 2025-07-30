from pydantic import BaseModel

from constants.stats import Stat
from constants.status import NonVolatileStatus, VolatileStatus
from constants.types import PokemonType
from model.ability import Ability
from model.item import Item
from model.move import Move
from util import stat_calc_util


class Pokemon(BaseModel):
    name: str
    types: tuple[PokemonType, PokemonType]
    move: list[Move]
    ability: Ability
    held_item: Item | None = None
    base_hp: int
    base_attack: int
    base_defense: int
    base_speed: int
    base_special_attack: int
    base_special_defense: int
    hp_lost: int = 0

    stat_changes: dict[Stat, int] | None = None
    non_volatile_status: NonVolatileStatus | None = None
    volatile_status: list[VolatileStatus] = []

    @property
    def current_hp(self) -> int:
        return self.max_hp - self.hp_lost

    @property
    def max_hp(self) -> int:
        return stat_calc_util.base_hp(self.base_hp)

    @property
    def attack(self) -> int:
        return stat_calc_util.true_stat(self.base_attack)

    @property
    def defense(self) -> int:
        return stat_calc_util.true_stat(self.base_defense)

    @property
    def special_attack(self) -> int:
        return stat_calc_util.true_stat(self.base_special_attack)

    @property
    def special_defense(self) -> int:
        return stat_calc_util.true_stat(self.base_special_defense)

    @property
    def speed(self) -> int:
        return stat_calc_util.true_stat(self.base_speed)

    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0
