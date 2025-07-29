from model.ability import Ability
from model.effect import Effect
from constants.stats import Stat

Intimidate = Ability(
    name = 'Intimidate',
    on_enter_effects = [Effect.Modify_Stats(-1, 'opponent', Stat.ATTACK)]
)