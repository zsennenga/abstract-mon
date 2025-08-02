from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.status import NonVolatileStatus
from constants.types import PokemonType
from model.effect import Effect
from model.effects import DoMoveDamage, InflictStatus
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
        InflictStatus(status_condition=NonVolatileStatus.PARALYZE, chance=10),
    ]
