from enum import Enum


class NonVolatileStatus(Enum):
    NONE = 'none'
    DEAD = "dead"
    SLEEP = "sleep"
    PARALYZE = "paralyze"
    POISON = "poison"
    TOXIC = "toxic"
    BURN = "burn"
    FREEZE = "freeze"


class VolatileStatus(Enum):
    # TODO expand later
    CONFUSE = "confuse"
