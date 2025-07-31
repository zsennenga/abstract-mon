import factory
from factory import SubFactory

from constants.trainer_side_identifier import TrainerSideIdentifier
from model.trainer import OpponentTrainer, PlayerTrainer
from tests.factories.pokemon_factory import PokemonFactory


class PlayerTrainerFactory(factory.Factory[PlayerTrainer]):
    class Meta:
        model = PlayerTrainer

    trainer_side_identifier = TrainerSideIdentifier.PLAYER
    name = "Player Trainer"
    party = factory.List([SubFactory(PokemonFactory)])
    _active_pokemon_index = 0


class OpponentTrainerFactory(factory.Factory[OpponentTrainer]):
    class Meta:
        model = OpponentTrainer

    trainer_side_identifier = TrainerSideIdentifier.OPPONENT
    name = "Opponent Trainer"
    party = factory.List([SubFactory(PokemonFactory)])
    _active_pokemon_index = 0
