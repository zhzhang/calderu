from enum import Enum, IntEnum


class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


RANK_TO_CHIPS = {
    Rank.TWO: 2,
    Rank.THREE: 3,
    Rank.FOUR: 4,
    Rank.FIVE: 5,
    Rank.SIX: 6,
    Rank.SEVEN: 7,
    Rank.EIGHT: 8,
    Rank.NINE: 9,
    Rank.TEN: 10,
    Rank.JACK: 10,
    Rank.QUEEN: 10,
    Rank.KING: 10,
    Rank.ACE: 11,
}


class Suite(Enum):
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4


class Card:
    def __init__(self, rank: Rank, suite: Suite, chips: int):
        self.rank = rank
        self.suite = suite
        self.chips = chips

    def __str__(self):
        return f"{self.rank.name} of {self.suite.name}"

    def __repr__(self):
        return f"{self.rank.name} of {self.suite.name}"


DEFAULT_DECK = [
    Card(rank, suite, RANK_TO_CHIPS[rank]) for rank in Rank for suite in Suite
]
