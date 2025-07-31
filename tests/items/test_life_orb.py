import unittest

from items.life_orb import LifeOrb
from model.battle_state import BattleState
from model.modifier import ModifierContainer
from tests.factories.battle_factory import BattleFactory
from util.math_util import bound_positive_int


class TestLifeOrb(unittest.TestCase):
    def test_basic_life_orb(self) -> None:
        battle = BattleFactory.create()
        trainer_pokemon = battle.trainer_player_side.active_pokemon
        opponent_pokemon = battle.trainer_opponent_side.active_pokemon
        move = trainer_pokemon.moves[0]
        self.assertEqual(trainer_pokemon.damage_taken, 0)
        self.assertEqual(opponent_pokemon.damage_taken, 0)
        move.process_move(
            pokemon_active=trainer_pokemon,
            pokemon_inactive=opponent_pokemon,
            battle_state=BattleState(),
            modifier_container=ModifierContainer(),
        )
        self.assertEqual(trainer_pokemon.damage_taken, 0)
        base_damage_dealt = opponent_pokemon.damage_taken
        trainer_pokemon.held_item = LifeOrb()
        move.process_move(
            pokemon_active=trainer_pokemon,
            pokemon_inactive=opponent_pokemon,
            battle_state=BattleState(),
            modifier_container=ModifierContainer(),
        )
        self.assertEqual(
            opponent_pokemon.damage_taken,
            bound_positive_int(base_damage_dealt + 1.3 * base_damage_dealt),
        )
        self.assertEqual(
            trainer_pokemon.damage_taken,
            bound_positive_int(0.1 * trainer_pokemon.max_hp),
        )
