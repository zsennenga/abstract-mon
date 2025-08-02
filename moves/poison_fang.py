from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.status import NonVolatileStatus
from constants.types import PokemonType
from model.effect import Effect  # Needed for correct effects typing
from model.effects.chance_effect import ChanceEffect
from model.effects.do_damage import DoMoveDamage
from model.effects.inflict_status import InflictStatus
from model.move import Move


class PoisonFang(Move):
    """
    Poison Fang – Poison-type physical attack with a 50 % chance to badly poison
    the target.
    """

    # Core metadata
    name: str = "Poison Fang"
    type: PokemonType = PokemonType.POISON
    move_category: MoveCategory = MoveCategory.PHYSICAL

    # Stats used in damage calculation
    attack_stat: Stat = Stat.ATTACK
    defense_stat: Stat = Stat.DEFENSE

    # Base parameters
    power: int = 50
    accuracy: int = 100
    priority: int = 0

    # Effects executed when the move processes
    effects: list[Effect] = [
        DoMoveDamage(),
        ChanceEffect(
            chance=50,
            inner_effect=InflictStatus(
                status_condition=NonVolatileStatus.TOXIC,
            ),
        ),
    ]
