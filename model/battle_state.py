from pydantic import BaseModel

from model.terrain import Terrain
from model.weather import Weather


class BattleState(BaseModel):
    weather: Weather | None = None
    terrain: Terrain | None = None

    damage_dealt_this_turn: int = 0
