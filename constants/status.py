from enum import Enum


class NonVolatileStatus(Enum):
    SLEEP = "sleep"
    PARALYZE = "paralyze"
    POISON = "poison"
    BURN = "burn"
    FREEZE = "freeze"


class VolatileStatus(Enum):
    # TODO expand later
    CONFUSE = "confuse"
