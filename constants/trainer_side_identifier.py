from enum import Enum
from typing import Self


class TrainerSideIdentifier(Enum):
    PLAYER = "player"
    OPPONENT = "opponent"

    def get_opposite(self) -> Self:
        if self == TrainerSideIdentifier.PLAYER:
            return TrainerSideIdentifier.OPPONENT
        elif self == TrainerSideIdentifier.OPPONENT:
            return TrainerSideIdentifier.PLAYER
        else:
            raise ValueError(f"Unknown side identifier: {self}")
