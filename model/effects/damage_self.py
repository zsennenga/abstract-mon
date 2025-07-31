from model.battle_state import BattleState
from model.effect import Effect
from model.modifier import ModifierContainer
from model.move import Move
from model.pokemon import Pokemon
from util.math_util import bound_positive_int


class DamageSelf(Effect):
    percentage: float = 0.0
    flat_amount: int = 0

    def process_effect(
        self,
        *,
        pokemon_active: Pokemon,
        pokemon_inactive: Pokemon,
        battle_state: BattleState,
        move: Move | None,
        modifier_container: ModifierContainer,
    ) -> None:
        pokemon_active.take_damage(self.flat_amount)
        pokemon_active.take_damage(
            bound_positive_int(self.percentage * pokemon_active.max_hp)
        )
