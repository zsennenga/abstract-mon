from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.effect import Effect

class Ability(BaseModel):
    name: str
    on_enter_effects: list[Effect] = []
    before_process_move: list[Effect] = []
    # TODO uhhhh draw the rest of the owl
