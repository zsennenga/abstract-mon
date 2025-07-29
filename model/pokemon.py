from pydantic import BaseModel

from constants.stats import Stat
from constants.status import NonVolatileStatus, VolatileStatus
from constants.types import PokemonType
from model import calculate
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
    max_hp: int = calculate.base_hp(base_hp)
    current_hp: int = max_hp
    attack: int = calculate.true_stat(base_attack)
    defense: int = calculate.true_stat(base_defense)
    speed: int = calculate.true_stat(base_speed)
    special_attack: int = calculate.true_stat(base_special_attack)
    special_defense: int = calculate.true_stat(base_special_defense)
    #EFFECTS
    stat_changes: dict[Stat, int] | None = None
    non_volatile_status: NonVolatileStatus = NonVolatileStatus.NONE
    volatile_status: list[VolatileStatus] = []

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def take_damage(self, damage: int) -> None:
        self.current_hp =- damage
        if self.current_hp <= 0:
            self.current_hp = 0
            self.non_volatile_status = NonVolatileStatus.DEAD

        return
