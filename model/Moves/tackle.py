from model.move import Move
from constants.types import PokemonType
from constants.move_tag import MoveTag


class Tackle(Move):
    name: 'Tackle'
    type: PokemonType.NORMAL
    power: 40
    tags: [MoveTag.CONTACT, MoveTag.PHYSICAL]
    accuracy: 100
    priority: 0
    effects: []
    modifiers: []