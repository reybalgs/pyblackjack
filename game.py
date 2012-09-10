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

    def adjust_strength(self, hand):
        """Returns an int strength, based on the hand passed as an argument"""
        strength = 0 # initialize to 0
        aces_total = 0 # total number of aces in the hand
        aces_lowered = 0 # soft aces lowered to 1
        for card in hand:
            if(card is 'king' or card is 'queen' or card is 'jack' or 
                    card == 10):
                # We have a card with a power of 10
                strength += 10
            elif card is 'ace':
                # We have an ace
                aces_total += 1
                if ((strength + 11) > 21):
                    # Adding 21 would bust, so the ace turns into 1
                    strength += 1
                    aces_lowered += 1
                else:
                    strength += 11
            else:
                # We have a numbered card
                strength += card
           
            # Now we need to check if we are supposedly bust, but let's check
            # first if we have an ace that we can lower
            if strength > 21:
                for card in hand:
                    if card is 'ace':
                        if aces_lowered < aces_total:
                            # We can still lower this ace
                            strength -= 10
                            aces_lowered += 1

        # Return the hand strength
        return strength

    def display_stats(self):
        """Displays game stats such as number of chips and hands played."""
        print '\n=====\nStats\n====='
        print 'Chips: ' + str(self.chips)
        print 'Hands played: ' + str(self.total_hands)
        print 'Hands won: ' + str(self.won_hands)
        print 'Hands lost: ' + str(self.lost_hands)
        print '\n'

    def display_cards(self):
        """Displays the cards of the dealer and the player."""
        # Dealer cards
        print '\n======\nDealer\n======'
        print 'Strength: ' + str(self.dealer_strength)
        print 'Cards: ',
        for card in self.dealer_cards:
            print str(card),
        print '\n'
        
        # Player cards
        print '\n======\nPlayer\n======'
        print 'Strength: ' + str(self.player_strength)
        print 'Cards: ',
        for card in self.player_cards:
            print str(card),
        print '\n'

    def round(self):
        """
        A game round. Called by the game class itself whenever the player wants
        to play a hand.

        Returns either 0 if the player loses, 1 if the player wins, and 2 if
        the round is a draw.
        """
        # First we need to ask the user for their wager
        while wager < 1 or wager > 1000:
            wager = input('Please input your wager (1-1000): ')
            if wager < 1 or wager > 1000:
                print 'Invalid input! Try again.'

        # Now let's draw a card for the dealer
        card = self.draw_card()
        self.dealer_cards.append(card)
        # Draw a card for the player
        card = self.draw_card()
        self.player_cards.append(card)

    def __init__(self, chips_start):
        """ Initialization function """
        # Set the starting chips of the player to the passed value
        self.player_chips = chips_start
        # Set the number of total hands played as well as won and lost hands
        self.total_hands = 0
        self.won_hands = 0
        self.lost_hands = 0
        # Initialize the hands of the dealer and the player
        self.dealer_cards = []
        self.player_cards = []
        # Initialize the hand strengths of the dealer and the player
        self.dealer_strength = 0
        self.player_strength = 0

        option = 'no'
        while not option is 'no':
            print 'Round ' + str(self.total_hands + 1)
            
            if self.round() == 1:
                # Round returned a 1, which means the player won
                # Increment the number of winning hands
                self.won_hands += 1
                print 'Congratulations, you won this round!'

            elif self.round() == 2:
                # Round returned a 2, which means the round was a draw
                print 'Push!'

            else:
                # Round returned a 0, which means the player lost
                # Increment the number of lost hands
                self.lost_hands = 0
                print 'Sorry, you lost!'

            # Increment the number of total hands
            self.total_hands += 1

            option = raw_input("Go for another round? [yes/no]: ")

