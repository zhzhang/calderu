import anthropic

from balatro.game import Game

SYSTEM_PROMPT = """
You are playing Balatro, a game based on Poker.
The goal of each round is to play hands to reach a certain total chips.

You will be given a list of poker cards.

You may select UP TO 5 cards to play or discard.
The possible commands are:
play <card1> <card2> ... <card5> - Play the selected cards and draw new ones from the deck.
discard <card1> <card2> ... <card5> - Discard the selected cards and draw new ones from the deck up to the original number of cards in hand.

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

The chips of each card participating in hand is added to the base chips before that total is multiplied by the multiplier.
Cards are only scored if they participate in the hand.

You must make a total of 300 chips within 4 hands and 3 discards to win.

When making a move, please respond first with the command you with to execute,
then with === as a separator, then your reasoning for the move.

You must win within the allotted hands and discards, or the world ends, so don't save any discards.
Discarding cards is a good way to create stronger hands, by searching the remaining deck for the best cards to play.
You should try to discard cards until you can make at least a flush.

The maximum number of cards you can select for play or discard from a hand is 5.

GAME STATE:
"""

ROUND_TRACK_PROMPT = """
You are on the round track. You may choose to play or skip the current round.
If you skip the current round, you receive a tag instead.
To play the current round, type "play".
To skip the current round, type "skip".
"""

ROUND_PROMPT = """
Available actions:
play <card1> <card2> ... <card5> - Play the selected cards and draw new ones from the deck.
"""

SHOP_PROMPT = """
You have reached the shop. You may purchase the following items:

To purchase an item, type "buy <item_type> <item_position>".
For example, to purchase the first item in the card section, type "buy card 1".
To purchase the second booster pack in the booster pack section, type "buy booster 2".
To purchase the first voucher in the voucher section, type "buy voucher 1".
To continue to the next round, type "next".
"""

BOOSTER_PROMPT = """
You have opened a booster pack! You may select cards from the booster pack.
To select a card, type "select <card_position>".
If you do not wish to select any cards, type "skip".
"""


def hand_to_string(hand):
    acc = ""
    for i, card in enumerate(hand):
        acc += f"{i+1}: {card['name']}\n"
    return acc


def decsribe_shop_object(obj):
    return f"Name: {obj['name']}. Description: {obj['description']}. Cost: {obj['cost']} dollars.\n"


def describe_pack_object(obj):
    return f"Name: {obj['name']}. Description: {obj['description']}.\n"


def build_state_string(state):
    acc = ""
    game_step = state["state"]
    if game_step in ["SELECTING_HAND"]:
        acc += hand_to_string(state["hand"])
        acc += f"Remaining hands: {state['hands_left']})\n"
        acc += f"Remaining discards: {state['discards_left']})\n"
    if game_step == "SHOP":
        acc += "Shop Cards:\n"
        for i, card in enumerate(state["shop_cards"]):
            acc += f"{i+1}: {decsribe_shop_object(card)}"
        acc += "Shop Boosters:\n"
        for i, booster in enumerate(state["shop_boosters"]):
            acc += f"{i+1}: {decsribe_shop_object(booster)}"
        acc += "Shop Vouchers:\n"
        for i, voucher in enumerate(state["shop_vouchers"]):
            acc += f"{i+1}: {decsribe_shop_object(voucher)}"
    if game_step == "BUFFOON_PACK":
        acc += "Booster Joker Cards:\n"
        for i, card in enumerate(state["pack_choices"]):
            acc += f"{i+1}: {describe_pack_object(card)}"
    acc += f"Current Money: {state['dollars']}\n"
    print(acc)
    return acc


def select_prompt(state):
    if state["state"] == "SHOP":
        return SHOP_PROMPT
    if state["state"] == "BUFFOON_PACK":
        return BOOSTER_PROMPT


def parse_cmd(cmd):
    cmd = cmd.strip()
    action, *rest = cmd.split(" ")
    if action == "buy":
        return {
            "action": action,
            "type": rest[0],
            "position": int(rest[1]),
        }
    elif action in ["play", "discard"]:
        return {
            "action": action,
            "positions": int(rest[0]),
        }
    elif action == "select":
        return {
            "action": action,
            "position": int(rest[0]),
        }
    elif action in ["skip", "next"]:
        return {
            "action": action,
        }


def generate_action(state):
    client = anthropic.Anthropic()
    state_string = build_state_string(state)
    state_prompt = f"{select_prompt(state)}\n{state_string}"
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": state_prompt}],
            }
        ],
    )
    cmd, reasoning = message.content[0].text.split("===")
    print(f"Command: {cmd}")
    print(f"Reasoning: {reasoning}")
    return parse_cmd(cmd)
