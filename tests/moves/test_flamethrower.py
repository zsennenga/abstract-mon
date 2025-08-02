import unittest
from unittest.mock import patch

from constants.status import NonVolatileStatus
from constants.types import PokemonType
from model.battle_state import BattleState
from model.modifier import ModifierContainer
from moves import Flamethrower
from tests.factories.pokemon_factory import PokemonFactory


class TestFlamethrower(unittest.TestCase):
    def setUp(self) -> None:
        """Set up the test environment before each test."""
        self.battle_state = BattleState()
        self.modifier_container = ModifierContainer()

        # Create a standard attacker and target
        self.attacker = PokemonFactory.create(
            types=(PokemonType.FIRE, PokemonType.FIRE), non_volatile_status=None
        )
        self.target = PokemonFactory.create(
            types=(PokemonType.NORMAL, PokemonType.NORMAL), non_volatile_status=None
        )

        # Reset damage counters
        self.battle_state.damage_dealt_this_turn = 0

        # Initialize the move
        self.move = Flamethrower()

    @patch("model.effects.inflict_status.InflictStatus._chance_roll", return_value=1)
    def test_burn_effect_success(self, _mock_chance_roll: object) -> None:
        """Test Flamethrower's burn effect (success case)."""
        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify damage and burn status
        self.assertGreater(self.target.damage_taken, 0)
        self.assertEqual(self.target.non_volatile_status, NonVolatileStatus.BURN)

    def test_status_immunity(self) -> None:
        """Test that burn isn't applied when target already has a status."""
        # Target already has a status
        self.target.non_volatile_status = NonVolatileStatus.SLEEP

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Verify damage but status remains SLEEP
        self.assertGreater(self.target.damage_taken, 0)
        self.assertEqual(self.target.non_volatile_status, NonVolatileStatus.SLEEP)

    def test_burn_effect_does_not_trigger(self) -> None:
        """
        Verify that in TEST_MODE the burn effect does *not* trigger when the
        random‐chance helper is *not* mocked.  Only damage should be applied.
        """
        # Sanity-check pre-conditions.
        self.assertIsNone(self.target.non_volatile_status)

        # Execute the move without any patching of `_chance_roll`.
        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )

        # Damage should always be dealt in TEST_MODE.
        self.assertGreater(self.target.damage_taken, 0)

        # Burn should *not* be applied because `_chance_roll` returns 100 in
        # TEST_MODE which is greater than the move's 10 % burn chance.
        self.assertIsNone(self.target.non_volatile_status)

    def test_type_effectiveness(self) -> None:
        """Test Flamethrower type effectiveness against different types."""
        # Reset
        self.battle_state.damage_dealt_this_turn = 0
        self.target.damage_taken = 0

        # Normal target (neutral)
        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )
        neutral_damage = self.battle_state.damage_dealt_this_turn

        # Reset for Grass target (2x damage).  Use NORMAL as a neutral second
        # type instead of ``None`` to avoid KeyErrors inside the type-chart
        # lookup logic, which currently expects both slots to contain a
        # ``PokemonType`` instance.
        self.battle_state.damage_dealt_this_turn = 0
        self.target.damage_taken = 0
        self.target.types = (PokemonType.GRASS, PokemonType.NORMAL)

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )
        super_effective_damage = self.battle_state.damage_dealt_this_turn

        # Reset for Water target (0.5x damage).  Again, provide a neutral
        # secondary typing to satisfy the lookup table.
        self.battle_state.damage_dealt_this_turn = 0
        self.target.damage_taken = 0
        self.target.types = (PokemonType.WATER, PokemonType.NORMAL)

        self.move.process_move(
            pokemon_active=self.attacker,
            pokemon_inactive=self.target,
            battle_state=self.battle_state,
            modifier_container=self.modifier_container,
        )
        not_very_effective_damage = self.battle_state.damage_dealt_this_turn

        # Verify type effectiveness
        self.assertAlmostEqual(super_effective_damage / neutral_damage, 2.0, places=1)
        self.assertAlmostEqual(
            not_very_effective_damage / neutral_damage, 0.5, places=1
        )
