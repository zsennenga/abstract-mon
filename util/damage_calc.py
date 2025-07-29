from model.move import Move
from model.pokemon import Pokemon
from random import randint
from constants.stats import Stat
from constants.move_tag import MoveTag

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

    modifier: float = 1

    # CHECK FOR CRIT
    CRIT_CHART = {0: 16, 1: 8, 2: 4, 3: 3, 4: 2, 5: 1}
    if Stat.CRITICAL not in active.stat_changes:
        active.stat_changes[Stat.CRITICAL] = 0

    crit = active.stat_changes[Stat.CRITICAL]

    if MoveTag.HIGH_CRIT in move.tags:
        crit += 1
        if crit > 5:
            crit = 5

    if randint(1, CRIT_CHART[crit]) == 1:
        is_crit = True
        modifier *= 2
    else:
        is_crit = False

    if is_crit:
        damage: float = (50 * attack_stat * move.power) / (22 * defense_stat)
    else:
        attack_stat
        temp2 = target.defense
        damage: float = 0

    # TODO: clean up this mess

    # RANDOM MODIFIER

    target.take_damage(int(damage))
    return
