from constants.move_tag import MoveTag
from constants.types import PokemonType
from model.move import Move

LEAF_BLADE = Move(
    name="Leaf Blade",
    type=PokemonType.GRASS,
    power=70,
    tags=[MoveTag.CONTACT, MoveTag.PHYSICAL, MoveTag.HIGH_CRIT],
)
