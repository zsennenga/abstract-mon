from enum import Enum

from constants.stats import Stat
from model.nature import Nature


class NatureEnum(Enum):
    ADAMANT = "Adamant"
    BASHFUL = "Bashful"
    BOLD = "Bold"
    BRAVE = "Brave"
    CALM = "Calm"
    CAREFUL = "Careful"
    DOCILE = "Docile"
    GENTLE = "Gentle"
    HARDY = "Hardy"
    HASTY = "Hasty"
    IMPISH = "Impish"
    JOLLY = "Jolly"
    LAX = "Lax"
    LONELY = "Lonely"
    MILD = "Mild"
    MODEST = "Modest"
    NAIVE = "Naive"
    NAUGHTY = "Naughty"
    QUIET = "Quiet"
    QUIRKY = "Quirky"
    RASH = "Rash"
    RELAXED = "Relaxed"
    SASSY = "Sassy"
    SERIOUS = "Serious"
    TIMID = "Timid"


NATURES = {
    NatureEnum.ADAMANT: Nature(
        name=NatureEnum.ADAMANT.value,
        stat_modifiers={
            Stat.ATTACK: 1.1,
            Stat.SPECIAL_ATTACK: 0.9,
        },
    ),
    NatureEnum.BASHFUL: Nature(name=NatureEnum.BASHFUL.value, stat_modifiers={}),
    NatureEnum.BOLD: Nature(
        name=NatureEnum.BOLD.value,
        stat_modifiers={
            Stat.ATTACK: 0.9,
            Stat.DEFENSE: 1.1,
        },
    ),
    NatureEnum.BRAVE: Nature(
        name=NatureEnum.BRAVE.value,
        stat_modifiers={
            Stat.ATTACK: 1.1,
            Stat.SPEED: 0.9,
        },
    ),
    NatureEnum.CALM: Nature(
        name=NatureEnum.CALM.value,
        stat_modifiers={
            Stat.ATTACK: 0.9,
            Stat.SPECIAL_DEFENSE: 1.1,
        },
    ),
    NatureEnum.CAREFUL: Nature(
        name=NatureEnum.CAREFUL.value,
        stat_modifiers={
            Stat.SPECIAL_ATTACK: 0.9,
            Stat.SPECIAL_DEFENSE: 1.1,
        },
    ),
    NatureEnum.DOCILE: Nature(name=NatureEnum.DOCILE.value, stat_modifiers={}),
    NatureEnum.GENTLE: Nature(
        name=NatureEnum.GENTLE.value,
        stat_modifiers={
            Stat.DEFENSE: 0.9,
            Stat.SPECIAL_DEFENSE: 1.1,
        },
    ),
    NatureEnum.HARDY: Nature(name=NatureEnum.HARDY.value, stat_modifiers={}),
    NatureEnum.HASTY: Nature(
        name=NatureEnum.HASTY.value,
        stat_modifiers={
            Stat.DEFENSE: 0.9,
            Stat.SPEED: 1.1,
        },
    ),
    NatureEnum.IMPISH: Nature(
        name=NatureEnum.IMPISH.value,
        stat_modifiers={
            Stat.DEFENSE: 1.1,
            Stat.SPECIAL_ATTACK: 0.9,
        },
    ),
    NatureEnum.JOLLY: Nature(
        name=NatureEnum.JOLLY.value,
        stat_modifiers={
            Stat.SPECIAL_ATTACK: 0.9,
            Stat.SPEED: 1.1,
        },
    ),
    NatureEnum.LAX: Nature(
        name=NatureEnum.LAX.value,
        stat_modifiers={
            Stat.DEFENSE: 1.1,
            Stat.SPECIAL_DEFENSE: 0.9,
        },
    ),
    NatureEnum.LONELY: Nature(
        name=NatureEnum.LONELY.value,
        stat_modifiers={
            Stat.ATTACK: 1.1,
            Stat.DEFENSE: 0.9,
        },
    ),
    NatureEnum.MILD: Nature(
        name=NatureEnum.MILD.value,
        stat_modifiers={
            Stat.DEFENSE: 0.9,
            Stat.SPECIAL_ATTACK: 1.1,
        },
    ),
    NatureEnum.MODEST: Nature(
        name=NatureEnum.MODEST.value,
        stat_modifiers={
            Stat.ATTACK: 0.9,
            Stat.SPECIAL_ATTACK: 1.1,
        },
    ),
    NatureEnum.NAIVE: Nature(
        name=NatureEnum.NAIVE.value,
        stat_modifiers={
            Stat.SPECIAL_DEFENSE: 0.9,
            Stat.SPEED: 1.1,
        },
    ),
    NatureEnum.NAUGHTY: Nature(
        name=NatureEnum.NAUGHTY.value,
        stat_modifiers={
            Stat.ATTACK: 1.1,
            Stat.SPECIAL_DEFENSE: 0.9,
        },
    ),
    NatureEnum.QUIET: Nature(
        name=NatureEnum.QUIET.value,
        stat_modifiers={
            Stat.SPECIAL_ATTACK: 1.1,
            Stat.SPEED: 0.9,
        },
    ),
    NatureEnum.QUIRKY: Nature(name=NatureEnum.QUIRKY.value, stat_modifiers={}),
    NatureEnum.RASH: Nature(
        name=NatureEnum.RASH.value,
        stat_modifiers={
            Stat.SPECIAL_ATTACK: 1.1,
            Stat.SPECIAL_DEFENSE: 0.9,
        },
    ),
    NatureEnum.RELAXED: Nature(
        name=NatureEnum.RELAXED.value,
        stat_modifiers={
            Stat.DEFENSE: 1.1,
            Stat.SPEED: 0.9,
        },
    ),
    NatureEnum.SASSY: Nature(
        name=NatureEnum.SASSY.value,
        stat_modifiers={
            Stat.SPECIAL_DEFENSE: 1.1,
            Stat.SPEED: 0.9,
        },
    ),
    NatureEnum.SERIOUS: Nature(name=NatureEnum.SERIOUS.value, stat_modifiers={}),
    NatureEnum.TIMID: Nature(
        name=NatureEnum.TIMID.value,
        stat_modifiers={
            Stat.ATTACK: 0.9,
            Stat.SPEED: 1.1,
        },
    ),
}
