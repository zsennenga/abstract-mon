from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from model.effect import Effect


class Item(BaseModel):
    name: str
    on_turn_start: Optional[list["Effect"]] = []
    before_process_move: Optional[list["Effect"]] = []
