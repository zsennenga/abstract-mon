from random import randint
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from constants.accuracy_stage_multipliers import ACCURACY_STAGE_MULTIPLIERS
from constants.move_modifier_type import MoveModifierType
from constants.move_tag import MoveTag
from constants.stats import Stat
from constants.types import PokemonType
from model.battle_state import BattleState
from model.effect import Effect
from model.modifier import ModifierContainer
from util.stat_stage_util import normalize_stage

if TYPE_CHECKING:
    from model.pokemon import Pokemon


class Move(BaseModel):
    name: str
    type: PokemonType
    power: float
    tags: list[MoveTag] = []
    accuracy: float
    priority: int
    effects: list[Effect]

    def process_move(
        self,
        *,
        pokemon_active: "Pokemon",
        pokemon_inactive: "Pokemon",
        battle_state: BattleState,
        modifier_container: ModifierContainer,
    ) -> None:
        # TODO probably want to construct all normalized stats here upfront...
        accuracy_stage = normalize_stage(
            pokemon_active.get_stat_stage(Stat.ACCURACY)
            + modifier_container.get_stat_stage(Stat.ACCURACY)
            - pokemon_inactive.get_stat_stage(Stat.EVASION)
            - modifier_container.get_stat_stage(Stat.EVASION)
        )

        accuracy_multiplier = (
            modifier_container.get_move_modifier(MoveModifierType.ACCURACY)
            * ACCURACY_STAGE_MULTIPLIERS[accuracy_stage]
        )
        accuracy_roll = randint(1, 100) * accuracy_multiplier
        if self.accuracy < accuracy_roll:
            return
        for effect in self.effects:
            effect.process_effect(
                pokemon_active=pokemon_active,
                pokemon_inactive=pokemon_inactive,
                battle_state=battle_state,
                move=self,
                modifier_container=modifier_container,
            )

    # Moves cannot be changed
    model_config = ConfigDict(frozen=True)
