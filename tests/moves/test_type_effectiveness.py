import unittest
from unittest.mock import patch

from constants.types import PokemonType
from model.battle_state import BattleState
from model.modifier import ModifierContainer
from moves import Surf
from tests.factories.pokemon_factory import PokemonFactory


class TestTypeEffectiveness(unittest.TestCase):
    def setUp(self) -> None:
        """Set up the test environment before each test."""
        self.battle_state = BattleState()
        self.modifier_container = ModifierContainer()

        # Create a standard attacker and target
        self.attacker = PokemonFactory.create(
            types=(PokemonType.NO_TYPE, PokemonType.NO_TYPE), non_volatile_status=None
        )
        self.target = PokemonFactory.create(
            types=(PokemonType.NO_TYPE, PokemonType.NO_TYPE), non_volatile_status=None
        )

        # Reset damage counters
        self.battle_state.damage_dealt_this_turn = 0

        # Initialize the move
        self.move = Surf()

    @patch("model.effects.do_damage.DoMoveDamage._crit_random", return_value=0)
    @patch("model.effects.do_damage.DoMoveDamage._damage_roll", return_value=1.0)
    def test_type_effectiveness(
        self, _mock_crit_roll: object, _mock_random_factor: object
    ) -> None:
        """Test that 2x 4x .5x & .25x damage are correct."""
        # Neutral Damage
        self.target.types = (PokemonType.NORMAL, PokemonType.NORMAL)

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )
        neutral_damage = self.battle_state.damage_dealt_this_turn
        print(f"Neutral Damage: {neutral_damage}")

        # Reset and use a different type target (2x Weak)
        self.battle_state.damage_dealt_this_turn = 0
        self.target.damage_taken = 0
        self.target.types = (PokemonType.FIRE, PokemonType.FLYING)

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        damage_2x = self.battle_state.damage_dealt_this_turn
        print(f"2x Damage: {damage_2x}")

        # Reset and use a different type target (4x Weak)
        self.battle_state.damage_dealt_this_turn = 0
        self.target.damage_taken = 0
        self.target.types = (PokemonType.FIRE, PokemonType.GROUND)

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        damage_4x = self.battle_state.damage_dealt_this_turn
        print(f"4x Damage: {damage_4x}")

        # Reset and use a different type target (2x Resist)
        self.battle_state.damage_dealt_this_turn = 0
        self.target.damage_taken = 0
        self.target.types = (PokemonType.GRASS, PokemonType.FLYING)

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        damage_half = self.battle_state.damage_dealt_this_turn
        print(f"Not Effective: {damage_half}")

        # Reset and use a different type target (4x Resist)
        self.battle_state.damage_dealt_this_turn = 0
        self.target.damage_taken = 0
        self.target.types = (PokemonType.GRASS, PokemonType.WATER)

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        damage_quarter = self.battle_state.damage_dealt_this_turn
        print(f"Barely Effective: {damage_quarter}")

        self.assertAlmostEqual(neutral_damage / damage_quarter, 4.0, delta=0.1)
        self.assertAlmostEqual(neutral_damage / damage_half, 2.0, delta=0.1)
        self.assertAlmostEqual(damage_2x / neutral_damage, 2.0, delta=0.1)
        self.assertAlmostEqual(damage_4x / neutral_damage, 4.0, delta=0.1)
