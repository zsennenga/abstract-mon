from pydantic import BaseModel

from constants.stats import Stat
from constants.status import NonVolatileStatus, VolatileStatus
from constants.types import PokemonType
from model.ability import Ability
from model.item import Item
from model.move import Move
from model.stat_container import StatContainer


class Pokemon(BaseModel):
    name: str
    damage_taken: int
    stats: StatContainer
    non_volatile_status: NonVolatileStatus
    volatile_status: list[VolatileStatus]
    types: tuple[PokemonType, PokemonType]
    moves: list[Move]
    ability: Ability
    held_item: Item | None

    @property
    def current_hp(self) -> int:
        return self.max_hp - self.damage_taken

    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0

    def take_damage(self, damage: int) -> None:
        self.damage_taken += damage

    @property
    def max_hp(self) -> int:
        return self.stats.get_leveled_stat(Stat.HP)
