import unittest
from unittest.mock import patch

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

    @patch(
        "model.effects.modify_stat_stage.ModifyStatStage._chance_roll",
        return_value=1,
    )
    def test_stat_reduction(self, _mock_chance_roll: object) -> None:
        """Shadow Ball should always lower the target's Sp. Def in TEST_MODE."""
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
