from pydantic import BaseModel

from constants.trainer_side_identifier import TrainerSideIdentifier
from model.battle_state import BattleState
from model.game_action import MoveAction, SwitchAction
from model.modifier import ModifierContainer
from model.pokemon import Pokemon
from model.trainer import OpponentTrainer, PlayerTrainer, Trainer


class Battle(BaseModel):
    trainer_player_side: PlayerTrainer
    trainer_opponent_side: OpponentTrainer
    battle_state: BattleState = BattleState()

    def run(self) -> None:
        # TODO if a pokemon doing an action dies gotta skip it.
        while (
            self.trainer_player_side.has_remaining_pokemon()
            and self.trainer_opponent_side.has_remaining_pokemon()
        ):
            # TODO cross-round effects
            modifier_container = ModifierContainer()
            # TODO round start effects
            #   - Weather
            #   - Items
            #   - abilities

            # TODO battle state can impact speed (tailwind, trick room)
            # This is clean for now though
            ordered_actions = sorted(
                [
                    self.trainer_opponent_side.choose_action(),
                    self.trainer_player_side.choose_action(),
                ]
            )
            for action in ordered_actions:
                self.battle_state.damage_dealt_this_turn = 0
                if (
                    not self.trainer_opponent_side.has_remaining_pokemon()
                    or not self.trainer_player_side.has_remaining_pokemon()
                ):
                    break
                actor = action.actor
                nonactor = actor.get_opposite()
                if isinstance(action, MoveAction):
                    # TODO handle before move actions
                    pokemon_player_map: dict[TrainerSideIdentifier, Pokemon] = {
                        TrainerSideIdentifier.PLAYER: self.trainer_player_side.active_pokemon,
                        TrainerSideIdentifier.OPPONENT: self.trainer_opponent_side.active_pokemon,
                    }
                    active_pokemon = pokemon_player_map[actor]
                    inactive_pokemon = pokemon_player_map[nonactor]
                    action.move.process_move(
                        pokemon_active=active_pokemon,
                        pokemon_inactive=inactive_pokemon,
                        battle_state=self.battle_state,
                        modifier_container=modifier_container,
                    )
                elif isinstance(action, SwitchAction):
                    # TODO check if they can switch
                    # you can't pick switch in choose if switching is blocked
                    # TODO some sort of general way to check if you can switch
                    trainer: Trainer
                    if actor == TrainerSideIdentifier.PLAYER:
                        trainer = self.trainer_player_side
                    elif actor == TrainerSideIdentifier.OPPONENT:
                        trainer = self.trainer_opponent_side
                    else:
                        raise Exception(f"WHAT THE FUCK unknown actor: '{actor}'")
                    # TODO check abilities too
                    trainer.switch_pokemon(action.next_index)
                    # TODO process on switch out actions
                    # Todo process on_enter effects of abilities and items
                else:
                    raise Exception(f"Fuck off with this {type(action)}")
