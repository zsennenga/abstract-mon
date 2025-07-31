import factory

from model.ability import Ability
from model.effect import Effect


class AbilityFactory(factory.Factory[Ability]):
    class Meta:
        model = Ability

    name = "Basic Ability"
    on_enter_effects: list[Effect] = []
    before_process_move: list[Effect] = []
