from abc import ABC, abstractmethod
from enum import Enum


class View(Enum):
    BLIND = 1
    ROUND = 2
    SHOP = 3


class TrackActions(Enum):
    PLAY = 1
    SKIP = 2


class CardValue(Enum):
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
    STONE = 15


class Suite(Enum):
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4


class Game:
    jokers = []
    deck = []
    hands = 5
    discards = 3
    view = View.TRACK
    hand = []


class RoundAction(Enum):
    PLAY = 1
    DISCARD = 2


class Round:
    def __init__(self):
        pass

    def action(self, selected_cards, action):
        pass

    def deal(self):
        pass


class Hand(ABC):

    @abstractmethod
    def check(self, cards: list[str]):
        pass

    @abstractmethod
    def value(self):
        pass


class HighCard(Hand):
    def check(self, cards: list[str]):
        return True

    def value(self):
        pass


class Pair(Hand):
    def check(self, cards: list[str]):
        pass

    def value(self):
        pass
