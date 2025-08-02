import unittest
from unittest.mock import patch

from constants.move_category import MoveCategory
from constants.stats import Stat
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

    def test_move_properties(self) -> None:
        """Test that Quick Attack has the correct properties."""
        self.assertEqual(self.move.name, "Quick Attack")
        self.assertEqual(self.move.type, PokemonType.NORMAL)
        self.assertEqual(self.move.power, 40)
        self.assertEqual(self.move.accuracy, 100)
        self.assertEqual(self.move.priority, 1)
        self.assertEqual(self.move.move_category, MoveCategory.PHYSICAL)
        self.assertEqual(self.move.attack_stat, Stat.ATTACK)
        self.assertEqual(self.move.defense_stat, Stat.DEFENSE)

    def test_priority_comparison(self) -> None:
        """Test that Quick Attack has higher priority than regular moves."""
        self.assertGreater(self.move.priority, self.regular_move.priority)

    @patch("model.effects.do_damage.DoMoveDamage._damage_roll", return_value=1.0)
    @patch(
        "model.effects.do_damage.DoMoveDamage._crit_random", return_value=100
    )  # No crit
    def test_damage_calculation(self, mock_crit, mock_damage_roll) -> None:
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
