from abc import ABC

from pydantic import BaseModel

from model.battle_state import BattleState
from model.move import Move
from model.pokemon import Pokemon


class Effect(ABC, BaseModel):
    def process_effect(
        self,
        *,
        pokemon_active: Pokemon,
        pokemon_inactive: Pokemon,
        battle_state: BattleState,
        move_used__mutable: Move | None,
    ) -> None:
        raise NotImplementedError()
