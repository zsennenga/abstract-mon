from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.types import PokemonType
from model.effect import Effect
from model.effects.do_damage import DoMoveDamage
from model.move import Move


class Pound(Move):
    """
    Pound is a basic Normal-type physical attack with no additional effects.
    """

    # --- Static move metadata (annotated for Pydantic) ---
    name: str = "Pound"
    type: PokemonType = PokemonType.NORMAL
    move_category: MoveCategory = MoveCategory.PHYSICAL

    # --- Stats used in damage calculation ---
    attack_stat: Stat = Stat.ATTACK
    defense_stat: Stat = Stat.DEFENSE

    # --- Base move parameters ---
    power: int = 40
    accuracy: int = 100
    priority: int = 0

    # --- Executed effects ---
    effects: list[Effect] = [DoMoveDamage()]
