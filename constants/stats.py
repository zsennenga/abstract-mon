from enum import Enum


class Stat(Enum):
    ATTACK = "attack"
    DEFENSE = "defense"
    HP = "HP"
    SPECIAL_ATTACK = "special_attack"
    SPECIAL_DEFENSE = "special_defense"
    SPEED = "speed"

    EVASION = "evasion"
    ACCURACY = "accuracy"
    CRITICAL = "critical"
