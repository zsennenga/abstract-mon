import os


def is_test() -> bool:
    return os.getenv("TEST_MODE") == "true"
