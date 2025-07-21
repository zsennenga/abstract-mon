from pydantic import BaseModel

from constants.player_identifier import PlayerIdentifier
from model.battle_state import BattleState
from model.game_action import MoveAction, SwitchAction
from model.trainer import Trainer

# 1. We do not support run lol
# 2. We do not support item in battle
# 3. Move or Switch


class Battle(BaseModel):
    trainer_client_side: Trainer
    trainer_opposite_side: Trainer
    battle_state: BattleState

    def do_action(self, action: MoveAction | SwitchAction) -> None:
        if isinstance(action, MoveAction):
            pass
        elif isinstance(action, SwitchAction):
            if action.actor == PlayerIdentifier.PLAYER:
                trainer = self.trainer_client_side
            elif action.actor == PlayerIdentifier.OPPONENT:
                trainer = self.trainer_opposite_side
            else:
                raise ValueError(
                    f"Fuck off with this trainer type: {type(action.actor)}"
                )
            trainer.switch_pokemon(action.next_index)
        else:
            raise Exception(f"Fuck off with this {type(action)}")
