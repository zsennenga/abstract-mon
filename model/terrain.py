from pydantic import BaseModel

from model.effect import Effect


class Terrain(BaseModel):
    remaining_rounds: int
    can_override: bool = True
    on_round_start: list[Effect] = []
    on_turn_start: list[Effect] = []
    before_move: list[Effect] = []
