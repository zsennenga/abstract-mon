import random
from typing import Literal

from pydantic import BaseModel

from constants.stats import Stat
from constants.trainer_side_identifier import TrainerSideIdentifier
from model.game_action import MoveAction, SwitchAction
from model.pokemon import Pokemon


class Trainer(BaseModel):
    trainer_side_identifier: TrainerSideIdentifier
    name: str
    party: list[Pokemon]
    _active_pokemon_index: int = 0

    def has_remaining_pokemon(self) -> bool:
        return any(self.alive_pokemon)

    def switch_pokemon(self, new_index: int) -> None:
        if len(self.party) > new_index - 1:
            raise ValueError(
                f"Dude holy shit that's not a pokemon at index {new_index} on switch"
            )
        new_pokemon = self.party[new_index]
        if not new_pokemon.is_alive:
            raise Exception(
                f"Holy shit it's dead what the fuck don't send it out, can't switch {new_index} in"
            )
        self._active_pokemon_index = new_index

    @property
    def active_pokemon(self) -> Pokemon:
        return self.party[self._active_pokemon_index]

    @property
    def alive_pokemon(self) -> list[Pokemon]:
        return [pokemon for pokemon in self.party if pokemon.is_alive]

    def choose_action(self) -> MoveAction | SwitchAction:
        move = random.choice(self.active_pokemon.moves)
        return MoveAction(
            actor=self.trainer_side_identifier,
            move=move,
            speed=self.speed,
        )

    @property
    def speed(self) -> int:
        if not self.active_pokemon:
            return 0
        return self.active_pokemon.stats.get_modified_stat(Stat.SPEED)


class PlayerTrainer(Trainer):
    trainer_side_identifier: Literal[TrainerSideIdentifier.PLAYER] = (
        TrainerSideIdentifier.PLAYER
    )


class OpponentTrainer(Trainer):
    trainer_side_identifier: Literal[TrainerSideIdentifier.OPPONENT] = (
        TrainerSideIdentifier.OPPONENT
    )
