from pydantic import BaseModel

from model.effect import Effect


class Item(BaseModel):
    name: str
    on_turn_start: list[Effect] = []
    before_use_move: list[Effect] = []
