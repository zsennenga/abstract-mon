from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.types import PokemonType
from model.effect import Effect
from model.effects.do_damage import DoMoveDamage
from model.move import Move


class Surf(Move):
    """
    Surf is a basic Water-type physical attack with no additional effects.
    """

    # --- Static move metadata (annotated for Pydantic) ---
    name: str = "Surf"
    type: PokemonType = PokemonType.WATER
    move_category: MoveCategory = MoveCategory.SPECIAL

    # --- Stats used in damage calculation ---
    attack_stat: Stat = Stat.SPECIAL_ATTACK
    defense_stat: Stat = Stat.SPECIAL_DEFENSE

    # --- Base move parameters ---
    power: int = 90
    accuracy: int = 100
    priority: int = 0

    # --- Executed effects ---
    effects: list[Effect] = [DoMoveDamage()]
