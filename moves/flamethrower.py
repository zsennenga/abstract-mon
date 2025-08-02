from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.status import NonVolatileStatus
from constants.types import PokemonType

# Effect imports pulled directly from their modules to avoid relying on an empty
# model.effects.__init__.
from model.effect import Effect  # Needed for effects field type annotation
from model.effects.chance_effect import ChanceEffect
from model.effects.do_damage import DoMoveDamage
from model.effects.inflict_status import InflictStatus
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
        ChanceEffect(
            chance=10,
            inner_effect=InflictStatus(
                status_condition=NonVolatileStatus.BURN,
            ),
        ),
    ]
