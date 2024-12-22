from abc import ABC, abstractmethod
from typing import List

from cards import Card


class Hand(ABC):
    def __init__(self, game):
        self.game = game

    @property
    @abstractmethod
    def chips(self):
        pass

    @property
    @abstractmethod
    def mult(self):
        pass

    @abstractmethod
    def check(self, cards: List[Card]) -> bool:
        pass


class HighCard(Hand):
    chips = 5
    mult = 1

    def __init__(self, game):
        self.game = game

    def check(self, cards: List[Card]) -> bool:
        return True


class Pair(Hand):
    chips = 10
    mult = 2

    def __init__(self, game):
        self.game = game

    def check(self, cards: List[Card]) -> bool:
        values = [card.rank for card in cards]
        for value in values:
            if values.count(value) == 2:
                return True


class TwoPair(Hand):
    chips = 20
    mult = 2

    def __init__(self, game):
        self.game = game

    def check(self, cards: List[Card]) -> bool:
        values = [card.rank for card in cards]
        pairs = 0
        for value in set(values):
            if values.count(value) == 2:
                pairs += 1
            if pairs == 2:
                return True


class ThreeOfAKind(Hand):
    chips = 30
    mult = 3

    def __init__(self, game):
        self.game = game

    def check(self, cards: List[Card]) -> bool:
        values = [card.rank for card in cards]
        for value in values:
            if values.count(value) == 3:
                return True


class Straight(Hand):
    chips = 30
    mult = 4

    def check(self, cards: List[Card]) -> bool:
        # TODO straight with ace at the bottom.
        values = [card.rank for card in cards]
        values.sort()
        for i, value in enumerate(values):
            if i == 0:
                continue
            if value - 1 != values[i - 1]:
                return False
        return True


class Flush(Hand):
    chips = 35
    mult = 4

    def check(self, cards: List[Card]) -> bool:
        suites = [card.suite for card in cards]
        for suite in suites:
            if suites.count(suite) == 5:
                return True


class FullHouse(Hand):
    chips = 40
    mult = 4

    def check(self, cards: List[Card]) -> bool:
        values = [card.rank for card in cards]
        for value in set(values):
            if values.count(value) == 3:
                for value in set(values):
                    if values.count(value) == 2:
                        return True


class FourOfAKind(Hand):
    chips = 60
    mult = 7

    def check(self, cards: List[Card]) -> bool:
        values = [card.rank for card in cards]
        for value in values:
            if values.count(value) == 4:
                return True


class StraightFlush(Hand):
    chips = 100
    mult = 8

    def check(self, cards: List[Card]) -> bool:
        straight_instance = next(
            filter(lambda x: x.__class__ == Straight, self.game.hand_instances), None
        )
        flush_instance = next(
            filter(lambda x: x.__class__ == Flush, self.game.hand_instances), None
        )
        assert straight_instance is not None and flush_instance is not None
        if straight_instance.check(cards) and flush_instance.check(cards):
            return True


class RoyalFlush(Hand):
    chips = 100
    mult = 8

    def check(self, cards: List[Card]) -> bool:
        straight_flush_instance = next(
            filter(lambda x: x.__class__ == StraightFlush, self.game.hand_instances),
            None,
        )
        assert straight_flush_instance is not None
        if straight_flush_instance.check(cards):
            values = [card.rank for card in cards]
            if values[0] == 10:
                return True


DEFAULT_HANDS = [
    RoyalFlush,
    StraightFlush,
    FourOfAKind,
    FullHouse,
    Flush,
    Straight,
    ThreeOfAKind,
    TwoPair,
    Pair,
    HighCard,
]
