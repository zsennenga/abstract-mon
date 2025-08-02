from constants.move_category import MoveCategory
from constants.stats import Stat
from constants.types import PokemonType
from model.effect import Effect

# Import concrete effect classes directly from their modules to avoid relying
# on aggregated exports in ``model.effects`` (which is now intentionally empty).
from model.effects.chance_effect import ChanceEffect
from model.effects.do_damage import DoMoveDamage
from model.effects.modify_stat_stage import ModifyStatStage
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
        ChanceEffect(
            chance=20,
            inner_effect=ModifyStatStage(
                stat=Stat.SPECIAL_DEFENSE,
                stage_change=-1,
                target="opponent",
            ),
        ),
    ]
