from abc import ABC, abstractmethod


class Joker(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def trigger(self):
        pass


class BaseJoker(Joker):
    """
    Adds 4 to the mult.
    """

    def __init__(self, game):
        super().__init__(game)

    def trigger(self):
        round = self.game.stage
        round.mult += 4


class Greedy(Joker):
    def __init__(self, game):
        super().__init__(game)


class Lusty(Joker):
    def __init__(self, game):
        super().__init__(game)


class Wrathful(Joker):
    def __init__(self, game):
        super().__init__(game)


class Gluttonous(Joker):
    def __init__(self, game):
        super().__init__(game)


class Jolly(Joker):
    def __init__(self, game):
        super().__init__(game)


class Zany(Joker):
    def __init__(self, game):
        super().__init__(game)


class Mad(Joker):
    def __init__(self, game):
        super().__init__(game)


class Crazy(Joker):
    def __init__(self, game):
        super().__init__(game)


class Droll(Joker):
    def __init__(self, game):
        super().__init__(game)


class Sly(Joker):
    def __init__(self, game):
        super().__init__(game)


class Wily(Joker):
    def __init__(self, game):
        super().__init__(game)


class Clever(Joker):
    def __init__(self, game):
        super().__init__(game)


class Devious(Joker):
    def __init__(self, game):
        super().__init__(game)


class Crafty(Joker):
    def __init__(self, game):
        super().__init__(game)
