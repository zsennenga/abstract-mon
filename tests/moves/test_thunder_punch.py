import unittest
from unittest.mock import patch

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

    @patch("model.effects.chance_effect.ChanceEffect._chance_roll", return_value=1)
    def test_paralyze_effect(self, _mock_chance_roll: object) -> None:
        """Thunder Punch should deal damage and always paralyze in TEST_MODE."""
        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify damage and paralyze status
        self.assertGreater(self.target.damage_taken, 0)
        self.assertEqual(self.target.non_volatile_status, NonVolatileStatus.PARALYZE)
