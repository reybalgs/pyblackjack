#
# pyblackjack/game.py
#
# This file contains most of the stuff concerning the game flow, logic and
# mechanics.

import random

class Game():
    """
    The main game class.

    The main main class (excuse the term) creates an instance of the Game class
    whenever the player starts with a new game.
    """
    def draw_card(self):
        """
        Draws a random card and returns its numerical/face value.
        """
        card = random.randint(1,10)

        # Now let's check what kind of card we have
        if card == 1:
            # 1 means ace, let's return that
            return 'ace'
        elif card > 1 and card < 10:
            # Card is a number between 2 to 9
            return card
        else:
            # Card is a 10 or a face card
            # Randomize again
            card = random.randint(1,4)
            # Now let's check if the card is a 10, jack, queen or king
            if card == 1:
                return 10
            elif card == 2:
                return 'jack'
            elif card == 3:
                return 'queen'
            else:
                return 'king'

    def __init__(self, chips_start):
        """ Initialization function """
        # Set the starting chips of the player to the passed value
        self.player_chips = chips_start
        # Set the number of total hands played as well as won and lost hands
        self.total_hands = 0
        self.won_hands = 0
        self.lost_hands = 0

