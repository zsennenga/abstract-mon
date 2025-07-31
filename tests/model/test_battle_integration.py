import unittest

from tests.factories.battle_factory import BattleFactory


class TestBattleIntegration(unittest.TestCase):
    def test_basic_battle(self) -> None:
        # Note: This doesn't actually do anything yet, it just tests that the battle terminates
        battle = BattleFactory.create()
        battle.run()
