from constants.types import PokemonType
from model.abilities.lazy import Lazy
from model.moves.leaf_blade import LEAF_BLADE
from model.moves.tackle import TACKLE
from model.pokemon import Pokemon

DONKEY = Pokemon(
    name="Donkey",
    base_hp=100,
    base_attack=100,
    base_defense=100,
    base_speed=100,
    base_special_attack=100,
    base_special_defense=100,
    types=(PokemonType.NORMAL, PokemonType.NO_TYPE),
    move=[TACKLE, LEAF_BLADE],
    ability=Lazy,
)
