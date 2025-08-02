from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.status import NonVolatileStatus
from constants.types import PokemonType
from model.effect import Effect

# Import concrete effect classes directly from their modules to avoid relying
# on aggregated exports in ``model.effects``.
from model.effects.chance_effect import ChanceEffect
from model.effects.do_damage import DoMoveDamage
from model.effects.inflict_status import InflictStatus
from model.move import Move


class ThunderPunch(Move):
    """
    Thunder Punch – Electric-type physical attack with a 10 % chance to paralyze
    the target.
    """

    # --- Static move metadata (annotated for Pydantic) ---
    name: str = "Thunder Punch"
    type: PokemonType = PokemonType.ELECTRIC
    move_category: MoveCategory = MoveCategory.PHYSICAL

    # Stats used for damage calculation
    attack_stat: Stat = Stat.ATTACK
    defense_stat: Stat = Stat.DEFENSE

    # Base parameters
    power: int = 75
    accuracy: int = 100
    priority: int = 0

    # Effects executed when the move processes
    effects: list[Effect] = [
        DoMoveDamage(),
        ChanceEffect(
            chance=10,
            inner_effect=InflictStatus(
                status_condition=NonVolatileStatus.PARALYZE,
            ),
        ),
    ]
