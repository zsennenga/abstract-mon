from random import randint
from typing import TYPE_CHECKING, Literal

from constants.stats import Stat
from model.effect import Effect
from util.setting_utils import is_test

if TYPE_CHECKING:
    from model.battle_state import BattleState
    from model.modifier import ModifierContainer
    from model.move import Move
    from model.pokemon import Pokemon


class ModifyStatStage(Effect):
    """
    Effect that modifies a stat stage of the target or user Pokemon with a specified chance.
    """

    # Pydantic model fields (no explicit __init__ required)
    stat: Stat
    stage_change: int
    target: Literal["self", "opponent"]
    chance: float

    def _chance_roll(self) -> int:
        """Return a random number between 1-100 for chance calculation."""
        if is_test():
            # In TEST_MODE return the maximum value so the effect does NOT
            # trigger unless tests explicitly override this helper via mocking,
            # keeping behaviour consistent with other random helpers.
            return 100
        return randint(1, 100)

    def process_effect(
        self,
        *,
        pokemon_active: "Pokemon",
        pokemon_inactive: "Pokemon",
        battle_state: "BattleState",
        move: "Move" = None,
        modifier_container: "ModifierContainer",
    ) -> None:
        """
        Process the stat stage modification.

        Args:
            pokemon_active: The Pokemon using the move
            pokemon_inactive: The target Pokemon
            battle_state: Current battle state
            move: The move being used
            modifier_container: Container for modifiers
        """
        # Check if the effect triggers based on chance
        if self._chance_roll() <= self.chance:
            # Apply to the correct Pokemon based on target
            if self.target == "self":
                target_pokemon = pokemon_active
            else:  # target == "opponent"
                target_pokemon = pokemon_inactive

            # Apply the stat stage change
            current_stage = target_pokemon.stats.get_stat_stage(self.stat)
            target_pokemon.stats.set_stat_stage(
                self.stat, current_stage + self.stage_change
            )
