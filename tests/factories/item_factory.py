import factory

from model.item import Item


class ItemFactory(factory.Factory):
    class Meta:
        model = Item

    name = "Basic Item"
    on_turn_start = []
    before_process_move = []
    after_damage_dealing_move = []
