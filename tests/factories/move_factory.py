import factory

from constants.move_category import MoveCategory
from constants.move_tag import MoveTag
from constants.stats import Stat
from constants.types import PokemonType
from model.effect import Effect
from model.effects.do_damage import DoMoveDamage
from model.move import Move


class MoveFactory(factory.Factory[Move]):
    class Meta:
        model = Move

    name = "Basic Move"
    type = PokemonType.NORMAL
    move_category = MoveCategory.PHYSICAL
    attack_stat = Stat.ATTACK
    defense_stat = Stat.DEFENSE
    power = 50
    tags: list[MoveTag] = []
    accuracy = 100
    priority = 0
    effects: list[Effect] = [DoMoveDamage()]
    requires_accuracy_roll = False  # Move should not miss
