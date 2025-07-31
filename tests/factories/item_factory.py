import factory

from model.effect import Effect
from model.item import Item


class ItemFactory(factory.Factory[Item]):
    class Meta:
        model = Item

    name = "Basic Item"
    on_turn_start: list[Effect] = []
    before_process_move: list[Effect] = []
    after_damage_dealing_move: list[Effect] = []
