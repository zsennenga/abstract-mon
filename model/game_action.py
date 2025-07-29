from pydantic import BaseModel

from constants.trainer_side_identifier import TrainerSideIdentifier
from model.move import Move


class MoveAction(BaseModel):
    actor: TrainerSideIdentifier
    move: Move


class SwitchAction(BaseModel):
    actor: TrainerSideIdentifier
    next_index: int
