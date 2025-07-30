from pydantic import BaseModel

from constants.stats import Stat
from constants.status import NonVolatileStatus, VolatileStatus
from constants.types import PokemonType
from model.ability import Ability
from model.item import Item
from model.move import Move


class Pokemon(BaseModel):
    name: str
    current_hp: int
    hp: int
    attack: int
    defense: int
    speed: int
    special_attack: int
    special_defense: int
    stat_changes: dict[Stat, int]
    non_volatile_status: NonVolatileStatus
    volatile_status: list[VolatileStatus]
    types: tuple[PokemonType, PokemonType]
    moves: list[Move]
    ability: Ability
    held_item: Item | None

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def get_stat_stage(self, stat: Stat) -> int:
        return self.stat_changes.get(stat, 0)
