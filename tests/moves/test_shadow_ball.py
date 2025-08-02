import unittest
from unittest.mock import patch

from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.types import PokemonType
from model.battle_state import BattleState
from model.modifier import ModifierContainer
from moves import ShadowBall
from tests.factories.pokemon_factory import PokemonFactory


class TestShadowBall(unittest.TestCase):
    def setUp(self) -> None:
        """Set up the test environment before each test."""
        self.battle_state = BattleState()
        self.modifier_container = ModifierContainer()

        # Create a standard attacker and target
        self.attacker = PokemonFactory.create(
            types=(PokemonType.GHOST, PokemonType.GHOST), non_volatile_status=None
        )
        self.target = PokemonFactory.create(
            # Use a type that can be hit by Ghost-type moves
            types=(PokemonType.PSYCHIC, PokemonType.PSYCHIC),
            non_volatile_status=None,
        )

        # Reset damage counters
        self.battle_state.damage_dealt_this_turn = 0

        # Initialize the move
        self.move = ShadowBall()

    def test_move_properties(self) -> None:
        """Test that Shadow Ball has the correct properties."""
        self.assertEqual(self.move.name, "Shadow Ball")
        self.assertEqual(self.move.type, PokemonType.GHOST)
        self.assertEqual(self.move.power, 80)
        self.assertEqual(self.move.accuracy, 100)
        self.assertEqual(self.move.priority, 0)
        self.assertEqual(self.move.move_category, MoveCategory.SPECIAL)
        self.assertEqual(self.move.attack_stat, Stat.SPECIAL_ATTACK)
        self.assertEqual(self.move.defense_stat, Stat.SPECIAL_DEFENSE)

    @patch("model.effects.do_damage.DoMoveDamage._damage_roll", return_value=1.0)
    @patch(
        "model.effects.do_damage.DoMoveDamage._crit_random", return_value=100
    )  # No crit
    @patch(
        "model.effects.modify_stat_stage.ModifyStatStage._chance_roll", return_value=1
    )  # Always apply effect
    def test_stat_reduction_success(
        self, mock_stat_roll, mock_crit, mock_damage_roll
    ) -> None:
        """Test Shadow Ball's Special Defense reduction (success case)."""
        # Set initial stat stage
        initial_sp_def = 0
        self.target.stats.set_stat_stage(Stat.SPECIAL_DEFENSE, initial_sp_def)

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify damage and stat reduction
        self.assertGreater(self.target.damage_taken, 0)
        self.assertEqual(
            self.target.stats.get_stat_stage(Stat.SPECIAL_DEFENSE), initial_sp_def - 1
        )

    @patch("model.effects.do_damage.DoMoveDamage._damage_roll", return_value=1.0)
    @patch(
        "model.effects.do_damage.DoMoveDamage._crit_random", return_value=100
    )  # No crit
    @patch(
        "model.effects.modify_stat_stage.ModifyStatStage._chance_roll", return_value=100
    )  # Never apply effect
    def test_stat_reduction_failure(
        self, mock_stat_roll, mock_crit, mock_damage_roll
    ) -> None:
        """Test Shadow Ball's Special Defense reduction (failure case)."""
        # Set initial stat stage
        initial_sp_def = 0
        self.target.stats.set_stat_stage(Stat.SPECIAL_DEFENSE, initial_sp_def)

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify damage but no stat reduction
        self.assertGreater(self.target.damage_taken, 0)
        self.assertEqual(
            self.target.stats.get_stat_stage(Stat.SPECIAL_DEFENSE), initial_sp_def
        )
