import unittest

from constants.stats import Stat
from tests.factories.pokemon_factory import StatContainerFactory


class TestStatContainers(unittest.TestCase):
    def setUp(self) -> None:
        self.test_container = StatContainerFactory.create()

    def test_correct_stats(self) -> None:
        "make sure stats are correct"
        self.assertEqual(341, self.test_container.get_leveled_stat(Stat.HP))
        self.assertEqual(236, self.test_container.get_leveled_stat(Stat.ATTACK))
        self.assertEqual(236, self.test_container.get_leveled_stat(Stat.DEFENSE))
        self.assertEqual(236, self.test_container.get_leveled_stat(Stat.SPEED))
        self.assertEqual(236, self.test_container.get_leveled_stat(Stat.SPECIAL_ATTACK))
        self.assertEqual(
            236, self.test_container.get_leveled_stat(Stat.SPECIAL_DEFENSE)
        )

    def test_stat_stages(self) -> None:
        # Test that increasing stat stages works correctly
        self.test_container.set_stat_stage(Stat.ATTACK, 1)

        plus_zero = self.test_container.get_leveled_stat(Stat.ATTACK)
        plus_one = self.test_container.get_modified_stat(Stat.ATTACK)

        self.assertGreater(plus_one, plus_zero)

        self.test_container.set_stat_stage(Stat.ATTACK, 6)
        plus_six = self.test_container.get_modified_stat(Stat.ATTACK)

        self.assertGreater(plus_six, plus_one)

    def test_stat_limit(self) -> None:
        # Test that stats can't go above +6
        self.test_container.set_stat_stage(Stat.ATTACK, 9)
        over_limit = self.test_container.get_modified_stat(Stat.ATTACK)

        self.test_container.set_stat_stage(Stat.ATTACK, 6)
        limit = self.test_container.get_modified_stat(Stat.ATTACK)

        self.assertEqual(limit, over_limit)
