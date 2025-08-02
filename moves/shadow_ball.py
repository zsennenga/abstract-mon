from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.types import PokemonType
from model.effect import Effect
from model.effects import DoMoveDamage, ModifyStatStage
from model.move import Move


class ShadowBall(Move):
    """
    Shadow Ball – Ghost-type special attack with a 20 % chance to lower the
    target's Special Defense by one stage.
    """

    # --- Static metadata (annotated for Pydantic) ---
    name: str = "Shadow Ball"
    type: PokemonType = PokemonType.GHOST
    move_category: MoveCategory = MoveCategory.SPECIAL

    # --- Stats used in damage calculation ---
    attack_stat: Stat = Stat.SPECIAL_ATTACK
    defense_stat: Stat = Stat.SPECIAL_DEFENSE

    # --- Base parameters ---
    power: int = 80
    accuracy: int = 100
    priority: int = 0

    # --- Executed effects ---
    effects: list[Effect] = [
        DoMoveDamage(),
        ModifyStatStage(
            stat=Stat.SPECIAL_DEFENSE,
            stage_change=-1,
            target="opponent",
            chance=20,
        ),
    ]
