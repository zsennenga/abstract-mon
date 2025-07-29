import random
from typing import TYPE_CHECKING

from pydantic import BaseModel

from constants.move_modifier_type import MoveModifierType
from constants.move_tag import MoveTag
from constants.types import PokemonType
from model.battle_state import BattleState
from model.effect import Effect
from model.move_modifier import MoveModifier

if TYPE_CHECKING:
    from model.pokemon import Pokemon


class Move(BaseModel):
    name: str
    type: PokemonType
    power: int
    tags: list[MoveTag] = []
    accuracy: float
    priority: float
    effects: list[Effect]
    modifiers: list[MoveModifier] = []

    def process_move(
        self,
        *,
        pokemon_active: "Pokemon",
        pokemon_inactive: "Pokemon",
        battle_state: BattleState,
    ) -> None:
        for modifier in self.modifiers:
            if modifier.modifier_type == MoveModifierType.ACCURACY:
                self.accuracy *= modifier.value
            elif modifier.modifier_type == MoveModifierType.POWER:
                self.power *= modifier.value
            else:
                raise NotImplementedError(
                    f"Unknown modifier type: {modifier.modifier_type} WHAT THE FUCK"
                )
        accuracy_roll = random.randint(1, 100)
        if self.accuracy < accuracy_roll:
            return
        for effect in self.effects:
            effect.process_effect(
                pokemon_active=pokemon_active,
                pokemon_inactive=pokemon_inactive,
                battle_state=battle_state,
                move_used__mutable=self,
            )
