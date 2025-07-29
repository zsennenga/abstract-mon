from abc import ABC
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

from model.battle_state import BattleState
from model.pokemon import Pokemon

if TYPE_CHECKING:
    from model.move import Move

class Effect(ABC, BaseModel):
    def process_effect(
        self,
        *,
        pokemon_active: Pokemon,
        pokemon_inactive: Pokemon,
        battle_state: BattleState,
        move_used__mutable: Optional["Move"],
    ) -> None:
        raise NotImplementedError()
