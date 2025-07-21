from typing import TYPE_CHECKING

from pydantic import BaseModel, PositiveInt

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
    tags: list[MoveTag] = []
    accuracy: PositiveInt
    priority: PositiveInt
    effects: list[Effect]
    modifiers: list[MoveModifier] = []

    def process_move(
        self,
        *,
        pokemon_active: "Pokemon",
        pokemon_inactive: "Pokemon",
        battle_state: BattleState,
    ) -> None:
        # TODO (GG) battle effects
        pass
