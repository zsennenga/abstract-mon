from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from model.effect import Effect


class Ability(BaseModel):
    name: str
    on_enter_effects: Optional[list["Effect"]] = []
    before_process_move: Optional[list["Effect"]] = []
    # TODO uhhhh draw the rest of the owl
