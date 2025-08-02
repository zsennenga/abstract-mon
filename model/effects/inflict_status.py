from random import randint
from typing import TYPE_CHECKING

from constants.status import NonVolatileStatus
from model.effect import Effect
from util.setting_utils import is_test

if TYPE_CHECKING:
    from model.battle_state import BattleState
    from model.modifier import ModifierContainer
    from model.move import Move
    from model.pokemon import Pokemon


class InflictStatus(Effect):
    """
    Effect that inflicts a non-volatile status condition on the target Pokemon with a specified chance.
    """

    # Pydantic fields – pydantic will auto-generate the __init__
    status_condition: NonVolatileStatus
    chance: float

    def _chance_roll(self) -> int:
        """Return a random number between 1-100 for chance calculation."""
        if is_test():
            return 1  # Always succeed in tests
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
        Process the status effect application.

        Args:
            pokemon_active: The Pokemon using the move
            pokemon_inactive: The target Pokemon
            battle_state: Current battle state
            move: The move being used
            modifier_container: Container for modifiers
        """
        # Skip if target already has a status
        if pokemon_inactive.non_volatile_status is not None:
            return

        # Check if the effect triggers based on chance
        if self._chance_roll() <= self.chance:
            pokemon_inactive.non_volatile_status = self.status_condition
