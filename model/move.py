from pydantic import BaseModel, PositiveInt

from constants.move_tag import MoveTag
from constants.types import PokemonType
from model.effect import Effect
from model.move_modifier import MoveModifier


class Move(BaseModel):
    name: str
    type: PokemonType
    tags: list[MoveTag] = []
    accuracy: PositiveInt
    priority: PositiveInt
    effects: list[Effect]
    modifiers: list[MoveModifier] = []
