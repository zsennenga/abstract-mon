from pydantic import BaseModel

from constants.player_identifier import PlayerIdentifier
from model.move import Move


class MoveAction(BaseModel):
    actor: PlayerIdentifier
    move: Move


class SwitchAction(BaseModel):
    actor: PlayerIdentifier
    next_index: int
