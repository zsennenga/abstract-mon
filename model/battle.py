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
            actions = {
                TrainerSideIdentifier.PLAYER: self.trainer_player_side.choose_action(),
                TrainerSideIdentifier.OPPONENT: self.trainer_opponent_side.choose_action(),
            }
            # TODO determine order
            # this is going to be more or less speed determined, with priority consideration
            # for now, lol just player/opponent
            # BUT ALSO pursuit means that actions can respond to actions fun
            action_order = list(actions.values())
            for action in action_order:
                if (
                    not self.trainer_opponent_side.has_remaining_pokemon()
                    or not self.trainer_player_side.has_remaining_pokemon()
                ):
                    break
                # TODO this is kinda janky maybe
                # like how I manage the actor and nonactor
                # I feel like there's something more elegant here
                # do trainers even need this value?
                # does this matter? like player/opponent.
                # There are two players, every action has an actor/nonactor
                # HRMMM
                if TrainerSideIdentifier.PLAYER == action.actor:
                    nonactor = TrainerSideIdentifier.OPPONENT
                elif TrainerSideIdentifier.OPPONENT == action.actor:
                    nonactor = TrainerSideIdentifier.PLAYER
                else:
                    raise Exception("tim robinson: 'what the fuck. WHAT THE FUCK'")
                if isinstance(action, MoveAction):
                    # TODO handle before move actions
                    pokemon_player_map: dict[TrainerSideIdentifier, Pokemon] = {
                        TrainerSideIdentifier.PLAYER: self.trainer_player_side.active_pokemon,
                        TrainerSideIdentifier.OPPONENT: self.trainer_opponent_side.active_pokemon,
                    }
                    active_pokemon = pokemon_player_map[action.actor]
                    inactive_pokemon = pokemon_player_map[nonactor]
                    # TODO should this be determined above?
                    # ... do trainers have an implicit speed from their pokemon?
                    pokemon_order: list[Pokemon] = [active_pokemon, inactive_pokemon]
                    for pokemon in pokemon_order:
                        for effect in pokemon.ability.before_process_move:
                            effect.process_effect(
                                pokemon_active=active_pokemon,
                                pokemon_inactive=inactive_pokemon,
                                battle_state=self.battle_state,
                                move=action.move,
                                modifier_container=modifier_container,
                            )
                        if pokemon.held_item:
                            for effect in pokemon.held_item.before_process_move:
                                effect.process_effect(
                                    pokemon_active=active_pokemon,
                                    pokemon_inactive=inactive_pokemon,
                                    battle_state=self.battle_state,
                                    move=action.move,
                                    modifier_container=modifier_container,
                                )
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
                    if action.actor == TrainerSideIdentifier.PLAYER:
                        trainer = self.trainer_player_side
                    elif action.actor == TrainerSideIdentifier.OPPONENT:
                        trainer = self.trainer_opponent_side
                    else:
                        raise Exception(
                            f"WHAT THE FUCK unknown actor: '{action.actor}'"
                        )
                    # TODO check abilities too
                    trainer.switch_pokemon(action.next_index)
                    # TODO process on switch out actions
                    # Todo process on_enter effects of abilities and items
                else:
                    raise Exception(f"Fuck off with this {type(action)}")
