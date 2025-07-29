from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.effect import Effect

class Item(BaseModel):
    name: str
    on_turn_start: list[Effect] = []
    before_process_move: list[Effect] = []
