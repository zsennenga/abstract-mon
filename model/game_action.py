from typing import Literal, Self

from pydantic import BaseModel

from constants.trainer_side_identifier import TrainerSideIdentifier
from model.move import Move


class GameAction(BaseModel):
    action_priority: int
    speed: int

    def __lt__(self, other: Self) -> bool:
        # Consider speed iff they have different priorities
        if self.action_priority == other.action_priority:
            return self.speed < other.speed
        return self.action_priority < other.action_priority


class MoveAction(GameAction):
    actor: TrainerSideIdentifier
    move: Move
    action_priority: Literal[0] = 0


class SwitchAction(GameAction):
    actor: TrainerSideIdentifier
    next_index: int
    action_priority: Literal[0] = 1
