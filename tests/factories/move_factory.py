import factory

from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.types import PokemonType
from model.move import Move


class MoveFactory(factory.Factory):
    class Meta:
        model = Move

    name = "Basic Move"
    type = PokemonType.NORMAL
    move_category = MoveCategory.PHYSICAL
    attack_stat = Stat.ATTACK
    defense_stat = Stat.DEFENSE
    power = 50
    tags = []
    accuracy = 100
    priority = 0
    effects = []
    requires_accuracy_roll = False  # Move should not miss
