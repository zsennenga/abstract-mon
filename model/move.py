import sys
from random import randint
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from constants.move_category import MoveCategory
from constants.move_modifier_type import MoveModifierType
from constants.move_tag import MoveTag
from constants.stat_stage_multipliers import ACCURACY_STAGE_MULTIPLIERS
from constants.stats import Stat
from constants.types import PokemonType
from model.battle_state import BattleState
from model.effect import Effect
from model.modifier import ModifierContainer
from util.math_util import bound_positive_int
from util.setting_utils import is_test
from util.stat_stage_util import normalize_stage

if TYPE_CHECKING:
    from model.pokemon import Pokemon


class Move(BaseModel):
    name: str
    type: PokemonType
    move_category: MoveCategory
    attack_stat: Stat
    defense_stat: Stat
    power: float = 0
    tags: list[MoveTag] = []
    accuracy: float = 100
    priority: int = 0
    effects: list[Effect] = []
    requires_accuracy_roll: bool = True

    def _accuracy_roll(self) -> int:
        if is_test():
            return sys.maxsize
        return randint(1, 100)

    def _accuracy_roll_passes(
        self,
        *,
        pokemon_active: "Pokemon",
        pokemon_inactive: "Pokemon",
        modifier_container: ModifierContainer,
    ) -> bool:
        # TODO probably want to construct all normalized stats here upfront...
        accuracy_stage = normalize_stage(
            pokemon_active.stats.get_stat_stage(Stat.ACCURACY)
            + modifier_container.get_stat_stage(Stat.ACCURACY)
            - pokemon_inactive.stats.get_stat_stage(Stat.EVASION)
            - modifier_container.get_stat_stage(Stat.EVASION)
        )

        accuracy_multiplier = (
            modifier_container.get_move_modifier(MoveModifierType.ACCURACY)
            * ACCURACY_STAGE_MULTIPLIERS[accuracy_stage]
        )
        accuracy_roll = self._accuracy_roll()
        if bound_positive_int(self.accuracy * accuracy_multiplier) < accuracy_roll:
            return False
        return True

    def process_move(
        self,
        *,
        pokemon_active: "Pokemon",
        pokemon_inactive: "Pokemon",
        battle_state: BattleState,
        modifier_container: ModifierContainer,
    ) -> None:
        pokemon_order = [
            pokemon_active,
            pokemon_inactive,
        ]
        for pokemon in pokemon_order:
            for effect in pokemon.ability.before_process_move:
                effect.process_effect(
                    pokemon_active=pokemon_active,
                    pokemon_inactive=pokemon_inactive,
                    battle_state=battle_state,
                    move=self,
                    modifier_container=modifier_container,
                )
            if pokemon.held_item:
                for effect in pokemon.held_item.before_process_move:
                    effect.process_effect(
                        pokemon_active=pokemon_active,
                        pokemon_inactive=pokemon_inactive,
                        battle_state=battle_state,
                        move=self,
                        modifier_container=modifier_container,
                    )
        if self.requires_accuracy_roll and not self._accuracy_roll_passes(
            pokemon_active=pokemon_active,
            pokemon_inactive=pokemon_inactive,
            modifier_container=modifier_container,
        ):
            return

        for effect in self.effects:
            effect.process_effect(
                pokemon_active=pokemon_active,
                pokemon_inactive=pokemon_inactive,
                battle_state=battle_state,
                move=self,
                modifier_container=modifier_container,
            )
        if battle_state.damage_dealt_this_turn > 0:
            for pokemon in pokemon_order:
                if not pokemon.held_item:
                    continue
                for effect in pokemon.held_item.after_damage_dealing_move:
                    effect.process_effect(
                        pokemon_active=pokemon_active,
                        pokemon_inactive=pokemon_inactive,
                        battle_state=battle_state,
                        move=self,
                        modifier_container=modifier_container,
                    )

    # Moves cannot be changed
    model_config = ConfigDict(frozen=True)
