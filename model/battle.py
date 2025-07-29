import copy

from pydantic import BaseModel

from constants.player_identifier import PlayerIdentifier
from model.battle_state import BattleState
from model.game_action import MoveAction, SwitchAction
from model.modifier import ModifierContainer
from model.pokemon import Pokemon
from model.trainer import Trainer


class Battle(BaseModel):
    trainer_player_side: Trainer
    trainer_opponent_side: Trainer
    battle_state: BattleState

    def do_action(
        self, action: MoveAction | SwitchAction, modifier_container: ModifierContainer
    ) -> None:
        if PlayerIdentifier.PLAYER == action.actor:
            nonactor = PlayerIdentifier.OPPONENT
        elif PlayerIdentifier.OPPONENT == action.actor:
            nonactor = PlayerIdentifier.PLAYER
        else:
            raise Exception("tim robinson: 'what the fuck. WHAT THE FUCK'")
        if isinstance(action, MoveAction):
            pokemon_player_map: dict[PlayerIdentifier, Pokemon] = {
                PlayerIdentifier.PLAYER: self.trainer_player_side.active_pokemon,
                PlayerIdentifier.OPPONENT: self.trainer_opponent_side.active_pokemon,
            }
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
                        move=move,
                        modifier_container=modifier_container,
                    )
                if pokemon.held_item:
                    for effect in pokemon.held_item.before_process_move:
                        effect.process_effect(
                            pokemon_active=active_pokemon,
                            pokemon_inactive=inactive_pokemon,
                            battle_state=self.battle_state,
                            move=move,
                            modifier_container=modifier_container,
                        )
            move.process_move(
                pokemon_active=active_pokemon,
                pokemon_inactive=inactive_pokemon,
                battle_state=self.battle_state,
                modifier_container=modifier_container,
            )
        elif isinstance(action, SwitchAction):
            if action.actor == PlayerIdentifier.PLAYER:
                trainer = self.trainer_player_side
            elif action.actor == PlayerIdentifier.OPPONENT:
                trainer = self.trainer_opponent_side
            else:
                raise Exception(f"WHAT THE FUCK unknown actor: '{action.actor}'")
            # TODO check abilities too
            trainer.switch_pokemon(action.next_index)
            # Todo process on_enter effects of abilities and items
        else:
            raise Exception(f"Fuck off with this {type(action)}")
