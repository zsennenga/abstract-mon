import factory

from constants.stats import Stat
from constants.status import NonVolatileStatus
from constants.types import PokemonType
from model.nature import Nature
from model.pokemon import Pokemon
from model.stat_container import StatContainer
from tests.factories.ability_factory import AbilityFactory
from tests.factories.item_factory import ItemFactory
from tests.factories.move_factory import MoveFactory


class NatureFactory(factory.Factory):
    class Meta:
        model = Nature

    name = "Hardy"
    stat_modifiers = {
        Stat.ATTACK: 1.0,
        Stat.DEFENSE: 1.0,
        Stat.SPECIAL_ATTACK: 1.0,
        Stat.SPECIAL_DEFENSE: 1.0,
        Stat.SPEED: 1.0,
    }


class StatContainerFactory(factory.Factory):
    class Meta:
        model = StatContainer

    level = 100
    nature = factory.SubFactory(NatureFactory)
    _base_hp = 100
    _base_attack = 100
    _base_defense = 100
    _base_speed = 100
    _base_special_attack = 100
    _base_special_defense = 100
    _stat_change_stages = {}


class PokemonFactory(factory.Factory):
    class Meta:
        model = Pokemon

    name = "Basic Pokemon"
    damage_taken = 0
    stats = factory.SubFactory(StatContainerFactory)
    non_volatile_status = NonVolatileStatus.SLEEP  # First enum value as default
    volatile_status = []
    types = (PokemonType.NORMAL, PokemonType.NORMAL)
    moves = factory.LazyFunction(lambda: [MoveFactory()])
    ability = factory.SubFactory(AbilityFactory)
    held_item = factory.SubFactory(ItemFactory)
