from random import randint
from typing import TYPE_CHECKING

from model.effect import Effect
from util.setting_utils import is_test

if TYPE_CHECKING:
    from model.battle_state import BattleState
    from model.modifier import ModifierContainer
    from model.move import Move
    from model.pokemon import Pokemon


class ChanceEffect(Effect):
    """
    A wrapper effect that executes an inner effect with a specified probability.

    This effect abstracts the chance-based logic away from individual effects,
    allowing for cleaner separation of concerns. The inner effect is only
    processed if a random roll is less than or equal to the specified chance.
    """

    # Pydantic model fields
    chance: float
    inner_effect: Effect

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
        move: "Move | None" = None,
        modifier_container: "ModifierContainer",
    ) -> None:
        """
        Process the effect with the specified chance.

        Args:
            pokemon_active: The Pokemon using the move
            pokemon_inactive: The target Pokemon
            battle_state: Current battle state
            move: The move being used
            modifier_container: Container for modifiers
        """
        # Check if the effect triggers based on chance
        if self._chance_roll() <= self.chance:
            # If successful, delegate to the inner effect
            self.inner_effect.process_effect(
                pokemon_active=pokemon_active,
                pokemon_inactive=pokemon_inactive,
                battle_state=battle_state,
                move=move,
                modifier_container=modifier_container,
            )
