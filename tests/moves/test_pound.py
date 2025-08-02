import unittest

from constants.types import PokemonType
from model.battle_state import BattleState
from model.modifier import ModifierContainer
from moves import Pound
from tests.factories.pokemon_factory import PokemonFactory


class TestPound(unittest.TestCase):
    def setUp(self) -> None:
        """Set up the test environment before each test."""
        self.battle_state = BattleState()
        self.modifier_container = ModifierContainer()

        # Create a standard attacker and target
        self.attacker = PokemonFactory.create(
            types=(PokemonType.NORMAL, PokemonType.NORMAL), non_volatile_status=None
        )
        self.target = PokemonFactory.create(
            types=(PokemonType.NORMAL, PokemonType.NORMAL), non_volatile_status=None
        )

        # Reset damage counters
        self.battle_state.damage_dealt_this_turn = 0

        # Initialize the move
        self.move = Pound()

    def test_damage_calculation(self) -> None:
        """Test that Pound deals the expected damage."""
        # Process the move
        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify damage was dealt
        self.assertGreater(self.target.damage_taken, 0)
        self.assertEqual(
            self.battle_state.damage_dealt_this_turn, self.target.damage_taken
        )

    def test_stab_bonus(self) -> None:
        """Test that STAB (Same Type Attack Bonus) is correctly applied."""
        # Normal attacker (STAB)
        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )
        normal_damage = self.battle_state.damage_dealt_this_turn

        # Reset and use a different type attacker (no STAB)
        self.battle_state.damage_dealt_this_turn = 0
        self.target.damage_taken = 0
        self.attacker.types = (PokemonType.FIRE, PokemonType.FIRE)

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        non_stab_damage = self.battle_state.damage_dealt_this_turn

        # STAB should be 1.5x damage
        self.assertAlmostEqual(normal_damage / non_stab_damage, 1.5, places=1)
