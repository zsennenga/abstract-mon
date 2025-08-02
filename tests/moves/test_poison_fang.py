import unittest
from unittest.mock import patch

from constants.status import NonVolatileStatus
from constants.types import PokemonType
from model.battle_state import BattleState
from model.modifier import ModifierContainer
from moves import PoisonFang
from tests.factories.pokemon_factory import PokemonFactory


class TestPoisonFang(unittest.TestCase):
    def setUp(self) -> None:
        """Set up the test environment before each test."""
        self.battle_state = BattleState()
        self.modifier_container = ModifierContainer()

        # Create a standard attacker and target
        self.attacker = PokemonFactory.create(
            types=(PokemonType.POISON, PokemonType.POISON), non_volatile_status=None
        )
        self.target = PokemonFactory.create(
            types=(PokemonType.NORMAL, PokemonType.NORMAL), non_volatile_status=None
        )

        # Reset damage counters
        self.battle_state.damage_dealt_this_turn = 0

        # Initialize the move
        self.move = PoisonFang()

    @patch("model.effects.chance_effect.ChanceEffect._chance_roll", return_value=1)
    def test_toxic_effect_applied(self, _mock_chance_roll: object) -> None:
        """Poison Fang should deal damage and badly poison the target in TEST_MODE."""
        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify damage and toxic status
        self.assertGreater(self.target.damage_taken, 0)
        self.assertEqual(self.target.non_volatile_status, NonVolatileStatus.TOXIC)

    def test_status_immunity(self) -> None:
        """Existing non-volatile status should prevent new Poison application."""
        self.target.non_volatile_status = NonVolatileStatus.SLEEP

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Damage still occurs, but status remains unchanged.
        self.assertGreater(self.target.damage_taken, 0)
        self.assertEqual(self.target.non_volatile_status, NonVolatileStatus.SLEEP)
