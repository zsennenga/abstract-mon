from pydantic import BaseModel

from constants.stats import Stat


class Nature(BaseModel):
    name: str
    stat_modifiers: dict[Stat, float]
