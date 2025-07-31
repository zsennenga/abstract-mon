from model.effects.damage_self import DamageSelf
from model.effects.multiply_damage import MultiplyDamage
from model.item import Item


class LifeOrb(Item):
    name = "Life Orb"
    before_process_move = [
        MultiplyDamage(multiplier=1.3),
    ]
    after_damage_dealing_move = [
        DamageSelf(
            percentage=0.1,
        )
    ]
