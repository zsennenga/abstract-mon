from pydantic import BaseModel

from model.terrain import Terrain
from model.weather import Weather


class BattleState(BaseModel):
    weather: Weather
    terrain: Terrain | None = None
