from model.ability import Ability

Intimidate = Ability(
    name="Intimidate",
    # on_enter_effects=[Effect.Modify_Stats.run(-1, Pokemon, Stat.ATTACK)]
    # TODO: implement this with new modifier system
)
