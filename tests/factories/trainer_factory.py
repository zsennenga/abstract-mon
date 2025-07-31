import factory

from constants.trainer_side_identifier import TrainerSideIdentifier
from model.trainer import OpponentTrainer, PlayerTrainer
from tests.factories.pokemon_factory import PokemonFactory


class PlayerTrainerFactory(factory.Factory):
    class Meta:
        model = PlayerTrainer

    trainer_side_identifier = TrainerSideIdentifier.PLAYER
    name = "Player Trainer"
    party = factory.LazyFunction(lambda: [PokemonFactory()])
    _active_pokemon_index = 0


class OpponentTrainerFactory(factory.Factory):
    class Meta:
        model = OpponentTrainer

    trainer_side_identifier = TrainerSideIdentifier.OPPONENT
    name = "Opponent Trainer"
    party = factory.LazyFunction(lambda: [PokemonFactory()])
    _active_pokemon_index = 0
