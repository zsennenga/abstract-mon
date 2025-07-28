# mypy: ignore-errors
import unittest

from constants.type_chart import TYPE_EFFECTIVENESS
from constants.types import PokemonType


class TestTypeChartCompleteness(unittest.TestCase):
    def test_type_chart_completeness(self):
        for type_ in PokemonType:
            with self.subTest(f"test_type_chart_completeness_{type_.name}"):
                chart = TYPE_EFFECTIVENESS[type_]
                for test_type in PokemonType:
                    self.assertIn(test_type, chart)
