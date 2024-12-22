from copy import copy
from enum import Enum
from random import shuffle
from typing import List

from cards import DEFAULT_DECK, RANK_TO_CHIPS
from hands import DEFAULT_HANDS


class View(Enum):
    BLIND = 1
    ROUND = 2
    SHOP = 3


class TrackActions(Enum):
    PLAY = 1
    SKIP = 2


ANTE_BASE = [100, 300, 800, 2000, 5000, 11000, 20000, 35000, 50000]


class RoundAction(Enum):
    PLAY = 1
    DISCARD = 2


class Game:
    ante = 1
    jokers = []
    full_deck = DEFAULT_DECK
    deck = []
    hands = 5
    discards = 3
    view = View.ROUND
    hand = []

    def __init__(self):
        self.score = 0
        self.hand_instances = [hand(self) for hand in DEFAULT_HANDS]
        deck = copy(self.full_deck)
        shuffle(deck)
        self.deck = deck

    def deal(self, n: int = 8):
        print(self.hand)
        for _ in range(n):
            tmp = self.deck.pop()
            self.hand.append(tmp)

    def action(self, selected_cards: List[int], action: RoundAction):
        selected_cards = [self.hand[card] for card in selected_cards]
        if action == RoundAction.PLAY:
            chips = 0
            mult = 0
            for hand_type in self.hand_instances:
                if hand_type.check(selected_cards):
                    print(hand_type)
                    chips = hand_type.chips
                    for card in selected_cards:
                        chips += card.chips
                    mult = hand_type.mult
                    break
            self.score += chips * mult
        print(self.score)

    def execute_command(self, command: str):
        command, *rest = command.split(" ")
        print(command, rest)
        if command == "p":
            selected_cards = [int(card) for card in rest]
            self.action(selected_cards, RoundAction.PLAY)


if __name__ == "__main__":
    game = Game()
    game.deal()
    while True:
        for i, card in enumerate(game.hand):
            print(f"{i}: {card}")
        command = input("Enter command:")
        game.execute_command(command)
