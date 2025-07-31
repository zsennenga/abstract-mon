from random import randint

from constants.move_category import MoveCategory
from constants.move_modifier_type import MoveModifierType
from constants.stat_stage_multipliers import CRIT_DENOMINATOR
from constants.stats import Stat
from constants.type_chart import TYPE_EFFECTIVENESS
from model.battle_state import BattleState
from model.effect import Effect
from model.modifier import ModifierContainer
from model.move import Move
from model.pokemon import Pokemon
from util.math_util import bound_positive_int
from util.setting_utils import is_test


class DoMoveDamage(Effect):
    def process_effect(
        self,
        *,
        pokemon_active: Pokemon,
        pokemon_inactive: Pokemon,
        battle_state: BattleState,
        move: Move | None,
        modifier_container: ModifierContainer,
    ) -> None:
        if move is None:
            raise ValueError("Only moves can deal move damage")
        damage = self._damage_calc(
            active=pokemon_active,
            target=pokemon_inactive,
            move=move,
            modifier_container=modifier_container,
        )
        # TODO add damage done modifiers
        pokemon_inactive.take_damage(damage)
        battle_state.damage_dealt_this_turn += damage
        # TODO after deal damage

    def _crit_random(self, crit_denominator: int) -> int:
        if is_test():
            return 0
        return randint(1, crit_denominator)

    def _damage_roll(self) -> float:
        if is_test():
            return 1.0
        return randint(85, 100) / 100

    def _damage_calc(
        self,
        *,
        active: Pokemon,
        target: Pokemon,
        move: Move,
        modifier_container: ModifierContainer,
    ) -> int:
        if move.power == 0 or move.move_category == MoveCategory.STATUS:
            return 0
        attack_stat = move.attack_stat
        defense_stat = move.defense_stat

        random_factor: float = self._damage_roll()

        stab_modifier = 1.0
        if move.type in active.types:
            stab_modifier *= 1.5

        type_effectiveness_1 = TYPE_EFFECTIVENESS[move.type][target.types[0]]
        type_effectiveness_2 = TYPE_EFFECTIVENESS[move.type][target.types[1]]

        if type_effectiveness_1 == 0 or type_effectiveness_2 == 0:
            return 0

        crit_stage = active.stats.get_stat_stage(Stat.CRITICAL)
        crit_denominator = CRIT_DENOMINATOR[crit_stage]

        if self._crit_random(crit_denominator) == 1:
            crit_damage_mod = 2
            defense_stat_value = target.stats.get_leveled_stat(defense_stat)
            attack_stat_value = active.stats.get_leveled_stat(attack_stat)
        else:
            crit_damage_mod = 1
            defense_stat_value = target.stats.get_modified_stat(defense_stat)
            attack_stat_value = active.stats.get_modified_stat(attack_stat)

        move_power_modifier = modifier_container.get_move_modifier(
            MoveModifierType.POWER
        )
        move_damage_modifier = modifier_container.get_move_modifier(
            MoveModifierType.DAMAGE
        )

        effective_power = bound_positive_int(move.power * move_power_modifier)

        base_damage = (50 * attack_stat_value * effective_power) / (
            22 * defense_stat_value
        )
        damage = (
            base_damage
            * crit_damage_mod
            * stab_modifier
            * type_effectiveness_1
            * type_effectiveness_2
            * move_damage_modifier
            * random_factor
        )
        return bound_positive_int(damage)
