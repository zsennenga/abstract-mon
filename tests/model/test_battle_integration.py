import unittest

from tests.factories.battle_factory import BattleFactory


class TestBattleIntegration(unittest.TestCase):
    def test_basic_battle(self) -> None:
        battle = BattleFactory.create()
        battle.run()
