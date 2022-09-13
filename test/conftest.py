import pytest


from utils.utils import fill_board


positions = [(5, "f"), (3, "d"), (2, "e"), (4, "h"),
             (5, "a"), (7, "c"), (1, "f"), (4, "d"),
             (3, "g"), (3, "e"), (4, "b"), (2, "a"),
             (0, "d"), (7, "a"), (0, "a"), (0, "f"),
             (5, "g"), (3, "b"), (7, "h"), (5, "c"),
             (7, "d"), (6, "b"), (7, "e"), (3, "h"),
             (2, "f"), (1, "h"), (7, "f"), (0, "e"),
             (1, "e"), (1, "g"), (4, "g"), (1, "b")]


@pytest.fixture(scope="session")
def board() -> dict[str, list]:
    return fill_board(positions)[0]


@pytest.fixture(scope="session")
def pieces() -> list:
    return fill_board(positions)[1]
