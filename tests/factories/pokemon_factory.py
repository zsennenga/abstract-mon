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


class NatureFactory(factory.Factory[Nature]):
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


class StatContainerFactory(factory.Factory[StatContainer]):
    class Meta:
        model = StatContainer

    level = 100
    nature = factory.SubFactory(NatureFactory)
    base_hp = 100
    base_attack = 100
    base_defense = 100
    base_speed = 100
    base_special_attack = 100
    base_special_defense = 100
    stat_change_stages: dict[Stat, int] = {}


class PokemonFactory(factory.Factory[Pokemon]):
    class Meta:
        model = Pokemon

    name = "Basic Pokemon"
    damage_taken = 0
    stats = factory.SubFactory(StatContainerFactory)
    non_volatile_status: NonVolatileStatus | None = None
    volatile_status: list[str] = []  # Assuming volatile status is a list of strings
    types = (PokemonType.NORMAL, PokemonType.NORMAL)
    moves = factory.List([factory.SubFactory(MoveFactory)])
    ability = factory.SubFactory(AbilityFactory)
    held_item = factory.SubFactory(ItemFactory)
