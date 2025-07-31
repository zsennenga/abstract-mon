from pydantic import BaseModel

from model.effect import Effect


class Item(BaseModel):
    name: str
    on_turn_start: list[Effect] = []
    before_process_move: list[Effect] = []
    after_damage_dealing_move: list[Effect] = []
