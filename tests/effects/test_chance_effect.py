import unittest
from unittest.mock import patch

from constants.stats import Stat
from constants.status import NonVolatileStatus
from model.battle_state import BattleState
from model.effects.chance_effect import ChanceEffect
from model.effects.inflict_status import InflictStatus
from model.effects.modify_stat_stage import ModifyStatStage
from model.modifier import ModifierContainer
from tests.factories.pokemon_factory import PokemonFactory


class TestChanceEffect(unittest.TestCase):
    def setUp(self) -> None:
        """Set up the test environment before each test."""
        self.battle_state = BattleState()
        self.modifier_container = ModifierContainer()

        # Create standard attacker and target
        self.attacker = PokemonFactory.create()
        self.target = PokemonFactory.create()

        # Create real effects for testing
        self.status_effect = InflictStatus(status_condition=NonVolatileStatus.BURN)

        self.stat_effect = ModifyStatStage(
            stat=Stat.ATTACK, stage_change=1, target="opponent"
        )

    def test_basic_instantiation(self) -> None:
        """Test that ChanceEffect can be instantiated with typical parameters."""
        # Create with real status effect
        effect = ChanceEffect(chance=10, inner_effect=self.status_effect)
        self.assertEqual(effect.chance, 10)
        self.assertEqual(effect.inner_effect, self.status_effect)
        self.assertEqual(effect.inner_effect.status_condition, NonVolatileStatus.BURN)

        # Create with real stat effect
        effect = ChanceEffect(chance=20, inner_effect=self.stat_effect)
        self.assertEqual(effect.chance, 20)
        self.assertEqual(effect.inner_effect, self.stat_effect)
        self.assertEqual(effect.inner_effect.stat, Stat.ATTACK)

    def test_effect_not_applied_in_test_mode_by_default(self) -> None:
        """Test that inner effect is not processed in TEST_MODE by default."""
        # Ensure target has no status initially
        self.target.non_volatile_status = None

        # Create effect with status effect
        effect = ChanceEffect(chance=50, inner_effect=self.status_effect)

        # Process without patching - should not apply status in TEST_MODE
        effect.process_effect(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify status was not applied
        self.assertIsNone(self.target.non_volatile_status)

    @patch("model.effects.chance_effect.ChanceEffect._chance_roll", return_value=1)
    def test_status_effect_applied_when_chance_succeeds(self, mock_chance_roll) -> None:
        """Test that status effect is processed when chance roll succeeds."""
        # Ensure target has no status initially
        self.target.non_volatile_status = None

        # Create effect with status effect
        effect = ChanceEffect(chance=50, inner_effect=self.status_effect)

        # Process with patched chance roll - should apply status
        effect.process_effect(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify status was applied
        self.assertEqual(self.target.non_volatile_status, NonVolatileStatus.BURN)

    @patch("model.effects.chance_effect.ChanceEffect._chance_roll", return_value=1)
    def test_stat_effect_applied_when_chance_succeeds(self, mock_chance_roll) -> None:
        """Test that stat effect is processed when chance roll succeeds."""
        # Set initial stat stage
        initial_stage = 0
        self.target.stats.set_stat_stage(Stat.ATTACK, initial_stage)

        # Create effect with stat effect
        effect = ChanceEffect(chance=50, inner_effect=self.stat_effect)

        # Process with patched chance roll - should apply stat change
        effect.process_effect(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify stat was modified
        self.assertEqual(
            self.target.stats.get_stat_stage(Stat.ATTACK), initial_stage + 1
        )
