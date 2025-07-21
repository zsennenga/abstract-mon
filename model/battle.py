import copy

from pydantic import BaseModel

from constants.player_identifier import PlayerIdentifier
from model.battle_state import BattleState
from model.game_action import MoveAction, SwitchAction
from model.pokemon import Pokemon
from model.trainer import Trainer

# 1. We do not support run lol
# 2. We do not support item in battle
# 3. Move or Switch


class Battle(BaseModel):
    trainer_player_side: Trainer
    trainer_opponent_side: Trainer
    battle_state: BattleState

    def do_action(self, action: MoveAction | SwitchAction) -> None:
        if isinstance(action, MoveAction):
            pokemon_player_map: dict[PlayerIdentifier, Pokemon] = {
                PlayerIdentifier.PLAYER: self.trainer_player_side.active_pokemon,
                PlayerIdentifier.OPPONENT: self.trainer_opponent_side.active_pokemon,
            }
            if PlayerIdentifier.PLAYER == action.actor:
                nonactor = PlayerIdentifier.OPPONENT
            elif PlayerIdentifier.OPPONENT == action.actor:
                nonactor = PlayerIdentifier.PLAYER
            else:
                raise Exception(
                    f"Fuck off with this unknown inactive actor {action.actor}"
                )
            active_pokemon = pokemon_player_map[action.actor]
            inactive_pokemon = pokemon_player_map[nonactor]
            move = copy.deepcopy(action.move)
            pokemon_order: list[Pokemon] = [active_pokemon, inactive_pokemon]
            for pokemon in pokemon_order:
                for effect in pokemon.ability.before_process_move:
                    effect.process_effect(
                        pokemon_active=active_pokemon,
                        pokemon_inactive=inactive_pokemon,
                        battle_state=self.battle_state,
                        move_used__mutable=move,
                    )
                if pokemon.held_item:
                    for effect in active_pokemon.held_item.ability.before_process_move:
                        effect.process_effect(
                            pokemon_active=active_pokemon,
                            pokemon_inactive=inactive_pokemon,
                            battle_state=self.battle_state,
                            move_used__mutable=move,
                        )
            move.process_move(
                pokemon_active=active_pokemon,
                pokemon_inactive=inactive_pokemon,
                battle_state=self.battle_state,
            )
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
            # Todo process on_enter effects of abilities and items
        else:
            raise Exception(f"Fuck off with this {type(action)}")
