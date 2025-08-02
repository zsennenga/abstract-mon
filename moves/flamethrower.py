from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.status import NonVolatileStatus
from constants.types import PokemonType
from model.effect import Effect  # Needed for effects field type annotation
from model.effects import DoMoveDamage, InflictStatus
from model.move import Move


class Flamethrower(Move):
    """
    Flamethrower is a Fire-type special attack with a 10 % chance to burn the target.
    """

    # Core move metadata
    name: str = "Flamethrower"
    type: PokemonType = PokemonType.FIRE
    move_category: MoveCategory = MoveCategory.SPECIAL

    # Stats used in damage calculation
    attack_stat: Stat = Stat.SPECIAL_ATTACK
    defense_stat: Stat = Stat.SPECIAL_DEFENSE

    # Base parameters
    power: int = 90
    accuracy: int = 100
    priority: int = 0

    # List of effects executed when the move is processed
    effects: list[Effect] = [
        DoMoveDamage(),
        InflictStatus(status_condition=NonVolatileStatus.BURN, chance=10),
    ]
