from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.types import PokemonType
from model.effect import Effect
from model.effects import DoMoveDamage
from model.move import Move


class QuickAttack(Move):
    """
    Quick Attack – a Normal-type physical move that gains +1 priority.
    """

    # --- Static move metadata (annotated for Pydantic) ---
    name: str = "Quick Attack"
    type: PokemonType = PokemonType.NORMAL
    move_category: MoveCategory = MoveCategory.PHYSICAL

    # Stats used for damage calculation
    attack_stat: Stat = Stat.ATTACK
    defense_stat: Stat = Stat.DEFENSE

    # Base move parameters
    power: int = 40
    accuracy: int = 100
    priority: int = 1

    # Move effects
    effects: list[Effect] = [DoMoveDamage()]
