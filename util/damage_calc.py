from random import randint

from constants.move_tag import MoveTag
from constants.stats import Stat
from constants.type_chart import TYPE_EFFECTIVENESS
from model.move import Move
from model.pokemon import Pokemon


def damage_calc(active: Pokemon, target: Pokemon, move: Move) -> int:
    if move.power == 0 or MoveTag.STATUS in move.tags:
        return 0

    if MoveTag.PHYSICAL in move.tags:
        attack_stat = active.attack
        defense_stat = target.defense
    elif MoveTag.SPECIAL in move.tags:
        attack_stat = active.special_attack
        defense_stat = target.special_defense
    else:
        raise ValueError("AH SHIT OH NO O DANGIT")

    modifier: float = 0.01 * randint(85, 100)

    if move.type in active.types:
        modifier *= 2

    modifier *= TYPE_EFFECTIVENESS[move.type][target.types[0]]
    modifier *= TYPE_EFFECTIVENESS[move.type][target.types[1]]

    # CHECK FOR CRIT
    crit_chart = {0: 16, 1: 8, 2: 4, 3: 3, 4: 2, 5: 1}
    crit = active.stat_changes.get(Stat.CRITICAL, 0)

    if MoveTag.HIGH_CRIT in move.tags:
        crit += 1
        if crit > 5:
            crit = 5

    if randint(1, crit_chart[crit]) == 1:
        is_crit = True
        modifier *= 2
    else:
        is_crit = False

    if is_crit:
        crit_damage = (50 * attack_stat * move.power) / (22 * defense_stat)
        return int(crit_damage)
    else:
        # TODO: make this work with stat changes
        # attack_stat = active.attack * active.stat_changes[Stat.ATTACK]
        # defense_stat = target.defense * target.stat_changes[Stat.DEFENSE]
        damage = (50 * attack_stat * move.power) / (22 * defense_stat)
        damage *= modifier
        return int(damage)

    # TODO: clean up this mess

    # RANDOM MODIFIER
