import factory

from model.battle import Battle
from model.battle_state import BattleState
from tests.factories.trainer_factory import OpponentTrainerFactory, PlayerTrainerFactory


class BattleFactory(factory.Factory[Battle]):
    class Meta:
        model = Battle

    trainer_player_side = factory.SubFactory(PlayerTrainerFactory)
    trainer_opponent_side = factory.SubFactory(OpponentTrainerFactory)
    battle_state = factory.LazyFunction(lambda: BattleState())
