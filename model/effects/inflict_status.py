from typing import TYPE_CHECKING

from constants.status import NonVolatileStatus
from model.effect import Effect

if TYPE_CHECKING:
    from model.battle_state import BattleState
    from model.modifier import ModifierContainer
    from model.move import Move
    from model.pokemon import Pokemon


class InflictStatus(Effect):
    """
    Effect that inflicts a non-volatile status condition on the target Pokemon.

    This is a simplified version without chance handling logic,
    meant to be used with ChanceEffect for probability handling.
    """

    # Pydantic field – pydantic will auto-generate the __init__
    status_condition: NonVolatileStatus

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

        # Apply the status (no chance check - handled by ChanceEffect if needed)
        pokemon_inactive.non_volatile_status = self.status_condition
