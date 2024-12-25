from copy import copy
from enum import Enum
from random import shuffle
from typing import List, Union

from balatro import jokers
from balatro.cards import DEFAULT_DECK, Card
from balatro.hands import DEFAULT_HANDS
from balatro.jokers import Joker


class Stage(Enum):
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


class Shop:
    cards: Union[Joker, Card] = []
    packs = []
    vouchers = []

    def __init__(self):
        # Select possible jokers to buy in the shop.
        pass


class Round:
    hand: List[Card] = []
    hands: int = 5
    discards: int = 3
    deck: List[Card] = []
    score: int = 0
    chips: int = 0
    mult: int = 0
    target: int = 300

    def __init__(self, game):
        self.game = game
        self.deck = copy(game.full_deck)
        shuffle(self.deck)
        self.deal()

    def reset(self):
        self.chips = 0
        self.mult = 0
        self.deal()

    def deal(self, hand_size: int = 8):
        while len(self.hand) < hand_size and len(self.deck) > 0:
            tmp = self.deck.pop()
            self.hand.append(tmp)

    def play(self, selected_card_idx: List[int]):
        assert self.hands > 0
        assert len(selected_card_idx) <= 5
        assert len(selected_card_idx) > 0
        self.hands -= 1
        selected_cards = [self.hand[card] for card in selected_card_idx]
        self.hand = [
            self.hand[card_idx]
            for card_idx in range(len(self.hand))
            if card_idx not in selected_card_idx
        ]
        for hand_type in self.game.hand_instances:
            hands_cards = hand_type.check(selected_cards)
            if hands_cards:
                self.chips = hand_type.chips
                for card in hands_cards:
                    self.chips += card.chips
                self.mult = hand_type.mult
                break
        # Trigger jokers.
        for joker in self.game.jokers:
            joker.trigger()
        self.score += self.chips * self.mult
        if self.score >= self.target:
            self.gold += 2 + self.hands
            self.game.stage = Shop()
        else:
            self.reset()

    def discard(self, selected_card_idx: List[int]):
        assert self.discards > 0
        self.discards -= 1
        self.hand = [
            self.hand[card_idx]
            for card_idx in range(len(self.hand))
            if card_idx not in selected_card_idx
        ]
        self.deal()

    def __str__(self):
        acc = ""
        for i, card in enumerate(self.hand):
            acc += f"{i}: {card}\n"
        acc += f"Score: {self.score}\n"
        acc += f"Remaining Hands: {self.hands}\n"
        acc += f"Remaining Discards: {self.discards}\n"
        if self.score >= 300:
            acc += "You win!\n"
        return acc


class Game:
    ante: int = 1
    money: int = 0
    jokers = []
    full_deck: List[Card] = DEFAULT_DECK
    stage: Union[Round, Shop]

    def __init__(self):
        self.score = 0
        self.hand_instances = [hand(self) for hand in DEFAULT_HANDS]
        self.stage = Round(self)
        self.jokers.append(jokers.BaseJoker(self))

    def action(self, selected_card_idx: List[int], action: RoundAction):
        if action == RoundAction.PLAY:
            assert isinstance(self.stage, Round)
            self.stage.play(selected_card_idx)
        elif action == RoundAction.DISCARD:
            assert isinstance(self.stage, Round)
            self.stage.discard(selected_card_idx)

    def __str__(self):
        acc = str(self.stage)
        acc += "Please response with your next action:\n"
        return acc

    def execute_command(self, command: str):
        command, *rest = command.split(" ")
        if command == "play":
            selected_cards = [int(card) for card in rest]
            self.action(selected_cards, RoundAction.PLAY)
        if command == "discard":
            selected_cards = [int(card) for card in rest]
            self.action(selected_cards, RoundAction.DISCARD)


if __name__ == "__main__":
    game = Game()
    while True:
        print(game)
        command = input("Enter command:")
        game.execute_command(command)
