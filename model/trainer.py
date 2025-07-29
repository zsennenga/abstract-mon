from pydantic import BaseModel

from model.pokemon import Pokemon


class Trainer(BaseModel):
    name: str
    party: list[Pokemon]
    _active_pokemon_index: int = 0

    def has_remaining_pokemon(self) -> bool:
        return any(self.alive_pokemon)

    def switch_pokemon(self, new_index: int) -> None:
        if len(self.party) > new_index - 1:
            raise ValueError(
                f"Dude holy shit that's not a pokemon at index {new_index} on switch"
            )
        new_pokemon = self.party[new_index]
        if not new_pokemon.is_alive():
            raise Exception(
                f"Holy shit it's dead what the fuck don't send it out, can't switch {new_index} in"
            )
        self._active_pokemon_index = new_index

    @property
    def active_pokemon(self) -> Pokemon:
        return self.party[self._active_pokemon_index]

    @property
    def alive_pokemon(self) -> list[Pokemon]:
        return [pokemon for pokemon in self.party if pokemon.is_alive()]
