from enum import Enum


class MoveTag(Enum):
    # https://bulbapedia.bulbagarden.net/wiki/Category:Moves_by_usage_method
    CONTACT = "contact"
    BOMB = "bomb"  # Mons with Bulletproof are Immune to these
    BITE = "bite"  # Buffed by Strong Jaw ability
    EXPLOSIVE = "explosive"  # Stopped by Damp ability
    POWDER = "powder"  # Grass types & Safety Goggles item & Overcoat ability are immune
    PULSE = "pulse"  # Buffed by Mega Launcher ability
    PUNCH = "punch"  # Buffed by Iron Fist ability & Punching Glove item
    SLICE = "slice"  # Buffed by Sharpness
    SOUND = "sound"  # Ignore Substitute, Soundproof are Immune, Buffed by Punk Rock, Change type with Liquid Voice
    WIND = "wind"  # Mons with Wind Rider are immune
