from model.effect import Effect
from model.effects.damage_self import DamageSelf
from model.effects.multiply_damage import MultiplyDamage
from model.item import Item


class LifeOrb(Item):
    name: str = "Life Orb"
    before_process_move: list[Effect] = [
        MultiplyDamage(multiplier=1.3),
    ]
    after_damage_dealing_move: list[Effect] = [
        DamageSelf(
            percentage=0.1,
        )
    ]
