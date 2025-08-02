from typing import TYPE_CHECKING, Literal

from constants.stats import Stat
from model.effect import Effect

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

    def process_effect(
        self,
        *,
        pokemon_active: "Pokemon",
        pokemon_inactive: "Pokemon",
        battle_state: "BattleState",
        move: "Move | None" = None,
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
        # Apply to the correct Pokemon based on target
        target_pokemon = pokemon_active if self.target == "self" else pokemon_inactive

        # Apply the stat stage change
        current_stage = target_pokemon.stats.get_stat_stage(self.stat)
        target_pokemon.stats.set_stat_stage(
            self.stat, current_stage + self.stage_change
        )
