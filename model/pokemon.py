from pydantic import BaseModel

from constants.stats import Stat
from constants.status import NonVolatileStatus, VolatileStatus
from constants.types import PokemonType
from util import calculate
from model.ability import Ability
from model.item import Item
from model.move import Move


class Pokemon(BaseModel):
    #MANDATORY
    name: str
    types: tuple[PokemonType, PokemonType]
    move: list[Move]
    ability: Ability | None
    held_item: Item | None
    #BASE STATS, ALSO MANDATORY
    base_hp: int
    base_attack: int
    base_defense: int
    base_speed: int
    base_special_attack: int
    base_special_defense: int
    #DERIVED STATS
    hp_lost: int = 0

    #EFFECTS
    stat_changes: dict[Stat, int] | None = None
    non_volatile_status: NonVolatileStatus = NonVolatileStatus.NONE
    volatile_status: list[VolatileStatus] = []

    @property
    def current_hp(self) -> int:
        return self.max_hp - self.hp_lost

    @property
    def max_hp(self) -> int:
        return calculate.base_hp(self.base_hp)

    @property
    def attack(self) -> int:
        return calculate.true_stat(self.base_attack)

    @property
    def defense(self) -> int:
        return calculate.true_stat(self.base_defense)

    @property
    def special_attack(self) -> int:
        return calculate.true_stat(self.base_special_attack)

    @property
    def special_defense(self) -> int:
        return calculate.true_stat(self.base_special_defense)

    @property
    def speed(self) -> int:
        return calculate.true_stat(self.base_speed)


    def is_alive(self) -> bool:
        return self.current_hp > 0

    def take_damage(self, damage: int) -> None:
        self.current_hp =- damage
        if self.current_hp <= 0:
            self.current_hp = 0
            self.non_volatile_status = NonVolatileStatus.DEAD

        return
