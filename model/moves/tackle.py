from constants.move_tag import MoveTag
from constants.types import PokemonType
from model.move import Move

TACKLE = Move(
    name="Tackle",
    type=PokemonType.NORMAL,
    power=40,
    tags=[MoveTag.CONTACT, MoveTag.PHYSICAL],
)
