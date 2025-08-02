import unittest
from unittest.mock import patch

from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.status import NonVolatileStatus
from constants.types import PokemonType
from model.battle_state import BattleState
from model.modifier import ModifierContainer
from moves import ThunderPunch
from tests.factories.pokemon_factory import PokemonFactory


class TestThunderPunch(unittest.TestCase):
    def setUp(self) -> None:
        """Set up the test environment before each test."""
        self.battle_state = BattleState()
        self.modifier_container = ModifierContainer()

        # Create a standard attacker and target
        self.attacker = PokemonFactory.create(
            types=(PokemonType.ELECTRIC, PokemonType.ELECTRIC), non_volatile_status=None
        )
        self.target = PokemonFactory.create(
            types=(PokemonType.NORMAL, PokemonType.NORMAL), non_volatile_status=None
        )

        # Reset damage counters
        self.battle_state.damage_dealt_this_turn = 0

        # Initialize the move
        self.move = ThunderPunch()

    def test_move_properties(self) -> None:
        """Test that Thunder Punch has the correct properties."""
        self.assertEqual(self.move.name, "Thunder Punch")
        self.assertEqual(self.move.type, PokemonType.ELECTRIC)
        self.assertEqual(self.move.power, 75)
        self.assertEqual(self.move.accuracy, 100)
        self.assertEqual(self.move.priority, 0)
        self.assertEqual(self.move.move_category, MoveCategory.PHYSICAL)
        self.assertEqual(self.move.attack_stat, Stat.ATTACK)
        self.assertEqual(self.move.defense_stat, Stat.DEFENSE)

    @patch("model.effects.do_damage.DoMoveDamage._damage_roll", return_value=1.0)
    @patch(
        "model.effects.do_damage.DoMoveDamage._crit_random", return_value=100
    )  # No crit
    @patch(
        "model.effects.inflict_status.InflictStatus._chance_roll", return_value=1
    )  # Always apply status
    def test_paralyze_effect_success(
        self, mock_status_roll, mock_crit, mock_damage_roll
    ) -> None:
        """Test Thunder Punch's paralyze effect (success case)."""
        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify damage and paralyze status
        self.assertGreater(self.target.damage_taken, 0)
        self.assertEqual(self.target.non_volatile_status, NonVolatileStatus.PARALYZE)

    @patch("model.effects.do_damage.DoMoveDamage._damage_roll", return_value=1.0)
    @patch(
        "model.effects.do_damage.DoMoveDamage._crit_random", return_value=100
    )  # No crit
    @patch(
        "model.effects.inflict_status.InflictStatus._chance_roll", return_value=100
    )  # Never apply status
    def test_paralyze_effect_failure(
        self, mock_status_roll, mock_crit, mock_damage_roll
    ) -> None:
        """Test Thunder Punch's paralyze effect (failure case)."""
        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify damage but no paralyze
        self.assertGreater(self.target.damage_taken, 0)
        self.assertIsNone(self.target.non_volatile_status)
