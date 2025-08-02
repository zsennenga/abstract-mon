import unittest

from constants.types import PokemonType
from model.battle_state import BattleState
from model.modifier import ModifierContainer
from moves import Pound, QuickAttack
from tests.factories.pokemon_factory import PokemonFactory


class TestQuickAttack(unittest.TestCase):
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

        # Initialize the moves
        self.move = QuickAttack()
        self.regular_move = Pound()

    def test_priority_comparison(self) -> None:
        """Test that Quick Attack has higher priority than regular moves."""
        self.assertGreater(self.move.priority, self.regular_move.priority)

    def test_damage_calculation(self) -> None:
        """Test that Quick Attack deals the expected damage."""
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
