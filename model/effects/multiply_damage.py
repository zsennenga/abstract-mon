from constants.move_modifier_type import MoveModifierType
from model.battle_state import BattleState
from model.effect import Effect
from model.modifier import ModifierContainer, MoveMagnitudeModifier
from model.move import Move
from model.pokemon import Pokemon


class MultiplyDamage(Effect):
    multiplier: float = 1.0

    def process_effect(
        self,
        *,
        pokemon_active: Pokemon,
        pokemon_inactive: Pokemon,
        battle_state: BattleState,
        move: Move | None,
        modifier_container: ModifierContainer,
    ) -> None:
        modifier_container.turn_modifier.append(
            MoveMagnitudeModifier(
                modifier_type=MoveModifierType.DAMAGE,
                value=self.multiplier,
            )
        )
