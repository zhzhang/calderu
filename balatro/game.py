from copy import copy
from enum import Enum
from random import shuffle
from typing import List

from .cards import DEFAULT_DECK, RANK_TO_CHIPS
from .hands import DEFAULT_HANDS


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

    def deal(self, hand_size: int = 8):
        while len(self.hand) < hand_size and len(self.deck) > 0:
            tmp = self.deck.pop()
            self.hand.append(tmp)

    def action(self, selected_card_idx: List[int], action: RoundAction):
        if action == RoundAction.PLAY:
            self.hands -= 1
            selected_cards = [self.hand[card] for card in selected_card_idx]
            self.hand = [
                self.hand[card_idx]
                for card_idx in range(len(self.hand))
                if card_idx not in selected_card_idx
            ]
            chips = 0
            mult = 0
            for hand_type in self.hand_instances:
                hands_cards = hand_type.check(selected_cards)
                if hands_cards:
                    chips = hand_type.chips
                    for card in hands_cards:
                        chips += card.chips
                    mult = hand_type.mult
                    break
            self.score += chips * mult
            self.deal()
        elif action == RoundAction.DISCARD:
            self.discards -= 1
            self.hand = [
                self.hand[card_idx]
                for card_idx in range(len(self.hand))
                if card_idx not in selected_card_idx
            ]
            self.deal()

    def __str__(self):
        acc = ""
        for card in self.hand:
            acc += f"{card}\n"
        acc += f"Score: {self.score}\n"
        if self.score >= 300:
            acc += "You win!"
        else:
            acc += "Please response with your next move:"
        return acc

    def execute_command(self, command: str):
        command, *rest = command.split(" ")
        print(command, rest)
        if command == "p":
            selected_cards = [int(card) for card in rest]
            self.action(selected_cards, RoundAction.PLAY)
        if command == "d":
            selected_cards = [int(card) for card in rest]
            self.action(selected_cards, RoundAction.DISCARD)


if __name__ == "__main__":
    game = Game()
    game.deal()
    print(game)
    while True:
        for i, card in enumerate(game.hand):
            print(f"{i}: {card}")
        command = input("Enter command:")
        game.execute_command(command)
