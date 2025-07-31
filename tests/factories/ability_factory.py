import factory

from model.ability import Ability


class AbilityFactory(factory.Factory):
    class Meta:
        model = Ability

    name = "Basic Ability"
    on_enter_effects = []
    before_process_move = []
