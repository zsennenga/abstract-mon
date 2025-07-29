def normalize_stage(stage: int) -> int:
    if stage > 6:
        return 6
    elif stage < -6:
        return -6
    return stage
