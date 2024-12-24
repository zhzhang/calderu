import anthropic

from balatro.game import Game

SYSTEM_PROMPT = """
You are playing Balatro, a game based on Poker.
The goal of each round is to play hands to reach a certain total chips.

You will be given a list of poker cards.

You may select UP TO 5 cards to play or discard.
The possible commands are:
p <card1> <card2> ... <card5> - Play the selected cards and draw new ones from the deck.
d <card1> <card2> ... <card5> - Discard the selected cards and draw new ones from the deck up to the original number of cards in hand.

For example: "p 1 2 3" with the following cards will play the first three cards:
0: FIVE of HEARTS
1: SEVEN of SPADES
2: TEN of SPADES
3: ACE of SPADES
4: EIGHT of CLUBS
5: FIVE of CLUBS
6: FOUR of DIAMONDS
7: SEVEN of HEARTS
which are the FIVE of HEARTS, SEVEN of SPADES, and TEN of SPADES.

The possible hands and their base chips are:
Pair: 10 chips * 2 multiplier
Two Pair: 20 chips * 2 multiplier
Three of a Kind: 30 chips * 3 multiplier
Straight: 30 chips * 4 multiplier
Flush: 35 chips * 4 multiplier
Full House: 40 chips * 4 multiplier
Four of a Kind: 60 chips * 7 multiplier
Straight Flush: 100 chips * 8 multiplier
Royal Flush: 100 chips * 8 multiplier

The maximum number of cards you can play in a hand is 5.

The chips of each card participating in hand is added to the base chips before that total is multiplied by the multiplier.
The chips for each rank of card are:
TWO: 2 chips
THREE: 3 chips
FOUR: 4 chips
FIVE: 5 chips
SIX: 6 chips
SEVEN: 7 chips
EIGHT: 8 chips
NINE: 9 chips
TEN: 10 chips
JACK: 10 chips
QUEEN: 10 chips
KING: 10 chips
ACE: 11 chips
Cards are only scored if they participate in the hand.

You must make a total of 300 chips within 4 hands and 3 discards to win.

When making a move, please respond first with the command you with to execute,
then with === as a separator, then your reasoning for the move.

You must win within the allotted hands and discards, or the world ends, so don't save any discards.
Discarding cards is a good way to create stronger hands, by searching the remaining deck for the best cards to play.
You should try to discard cards until you can make at least a flush.

GAME START
"""

client = anthropic.Anthropic()

game = Game()
game.deal()
while game.score < 300 and game.hands > 0:
    print(game)
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": str(game)}],
            }
        ],
    )
    cmd, reasoning = message.content[0].text.split("===")
    cmd = cmd.strip()
    print(cmd)
    print(reasoning)
    game.execute_command(cmd)
    print("--------------------")
