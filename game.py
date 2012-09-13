#
# pyblackjack/game.py
#
# This file contains most of the stuff concerning the game flow, logic and
# mechanics.

import random
import sys
import os
import pdb

class Game():
    """
    The main game class.

    The main main class (excuse the term) creates an instance of the Game class
    whenever the player starts with a new game.
    """
    def clear(self):
        """A little screen clearing function"""
        os.system("clear")

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

    def adjust_strength(self, hand, hidden_card = 0):
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
            elif card is '?':
                # We are dealing with a hidden card
                if (hidden_card is 'king' or hidden_card is 'queen' or 
                        hidden_card is 'jack' or hidden_card == 10):
                    strength += 10
                elif hidden_card is 'ace':
                    aces_total += 1
                    if ((strength + 11) > 21):
                        strength += 1
                        aces_lowered += 1
                    else:
                        strength += 11
                else:
                    strength += hidden_card
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
        print 'Chips: ' + str(self.player_chips)
        print 'Hands played: ' + str(self.total_hands)
        print 'Hands won: ' + str(self.won_hands)
        print 'Hands lost: ' + str(self.lost_hands)
        print '\n'

    def display_cards(self, dealer_strength, dealer_cards, player_strength,
            player_cards):
        """Displays the cards of the dealer and the player."""
        # Dealer cards
        print '\n======\nDealer\n======'
        print 'Strength: ' + str(dealer_strength)
        print 'Cards: ',
        for card in dealer_cards:
            print str(card) + ' ',
        print '\n'
        
        # Player cards
        print '\n======\nPlayer\n======'
        print 'Strength: ' + str(player_strength)
        print 'Cards: ',
        for card in player_cards:
            print str(card) + ' ',
        print '\n'

    def display_dealer_cards(self, dealer_strength, dealer_cards):
        """
        Displays the cards and strength of the dealer only. Could be useful in
        split plays.
        """
        print '\n======\nDealer\n======'
        print 'Strength: ' + str(dealer_strength)
        print 'Cards: ',
        for card in dealer_cards:
            print str(card) + ' ',
        print '\n'

    def display_split_cards(self, first_hand, first_strength, second_hand,
            second_strength):
        """Displays the two hands of the player after a split"""
        # First hand
        print '\n==========\nFirst Hand\n=========='
        print 'Strength: ' + str(first_strength)
        print 'Cards: ',
        for card in first_hand:
            print str(card) + ' ',
        print '\n'

        # Second hand
        print '\n===========\nSecond Hand\n==========='
        print 'Strength: ' + str(second_strength)
        print 'Cards: ',
        for card in second_hand:
            print str(card) + ' ',
        print '\n'

    def round(self):
        """
        A game round. Called by the game class itself whenever the player wants
        to play a hand.

        Returns either 0 if the player loses, 1 if the player wins, and 2 if
        the round is a draw.
        """
        # Temporary option var
        option = ''
        # Wager var
        wager = 0

        # Variables for dealer and player
        dealer_strength = 0
        dealer_cards = []
        player_strength = 0
        player_cards = []
        # Double hands
        first_hand = []
        first_strength = 0
        second_hand = []
        second_strength = 0

        self.display_stats()

        # First we need to ask the user for their wager
        while wager < 1 or wager > 1000:
            wager = input('Please input your wager (1-1000): ')
            if wager < 1 or wager > 1000:
                print 'Invalid input! Try again.'

        self.clear()
        # Decrease the chips with the wager
        self.player_chips -= wager

        self.display_stats()

        # Now let's draw a card for the dealer
        card = self.draw_card()
        dealer_cards.append(card)
        dealer_strength = self.adjust_strength(dealer_cards)
        self.display_cards(dealer_strength, dealer_cards, player_strength,
                player_cards)
        raw_input()
        self.clear()
        # Draw a card for the player
        card = self.draw_card()
        player_cards.append(card)
        player_strength = self.adjust_strength(player_cards)
        self.display_cards(dealer_strength, dealer_cards, player_strength,
                player_cards)
        raw_input()
        self.clear()
        # Draw a hidden card for the dealer
        card = self.draw_card()
        hidden_card = card
        dealer_cards.append('?')
        self.display_cards(dealer_strength, dealer_cards, player_strength,
                player_cards)
        raw_input()
        self.clear()
        # Draw the second card for the player
        card = self.draw_card()
        player_cards.append(card)
        player_strength = self.adjust_strength(player_cards)
        self.display_cards(dealer_strength, dealer_cards, player_strength,
                player_cards)
        raw_input()
        self.clear()

        # Now let's ask the player for input
        while (option != 's' and option != 'S') and player_strength < 21:
            self.display_cards(dealer_strength, dealer_cards, player_strength,
                    player_cards)
            if (player_cards[0] == player_cards[1] and 
                    (wager * 2 <= self.player_chips)):
                # Player can both split and double
                option = raw_input('Would you like to:\n\t[H]it' +
                        '\n\t[S]tay\n\t[D]ouble\n\ts[P]lit\nOption: ')
                if option is 'h' or option is 'H':
                    while player_strength < 21 and (option is not 's' and
                            option is not 'S'):
                        # Player wants to hit, draw another card
                        card = self.draw_card()
                        player_cards.append(card)
                        player_strength = self.adjust_strength(player_cards)
                        self.display_cards()
                        if player_strength < 21:
                            # Player isn't bust yet or got 21
                            option = raw_input('[H]it or [S]tay? ')

                elif option is 'p' or option is 'P':
                    # Player wants to split
                    # Double the player's wager
                    self.player_chips -= wager
                    wager = wager * 2
                    self.clear()
                    print 'Hand 1'
                    # Adjust the two new hands of the player
                    first_hand = [player_cards[0]]
                    first_strength = self.adjust_strength(first_hand)
                    second_hand = [player_cards[1]]
                    second_strength = self.adjust_strength(second_hand)
                    self.display_split_cards(first_hand,
                            first_strength, second_hand,
                            second_strength)
                    raw_input()
                    self.clear()
                    # Add a card to each of the two hands
                    # First hand
                    card = self.draw_card()
                    first_hand.append(card)
                    first_strength = self.adjust_strength(first_hand)
                    self.display_split_cards(first_hand, first_strength,
                            second_hand, second_strength)
                    raw_input()
                    self.clear()
                    # Second hand
                    card = self.draw_card()
                    second_hand.append(card)
                    second_strength = self.adjust_strength(second_hand)
                    self.display_split_cards(first_hand, first_strength,
                            second_hand, second_strength)
                    raw_input()
                    self.clear()

                    while first_strength < 21 and (option != 's' and option !=
                            'S'):
                        self.clear()
                        self.display_split_cards(first_hand, first_strength,
                                second_hand, second_strength)
                        print 'First hand: '
                        option = raw_input('[H]it or [D]ouble or [S]tay: ')
                        if option is 'h' or option is 'H':
                            card = self.draw_card()
                            first_hand.append(card)
                            first_strength = self.adjust_strength(first_hand)
                            self.display_split_cards(first_hand,
                                    first_strength, second_hand,
                                    second_strength)
                        elif option is 'd' or option is 'D':
                            card = self.draw_card()
                            first_hand.append(card)
                            first_strength = self.adjust_strength(first_hand)
                            self.display_split_cards(first_hand,
                                    first_strength, second_hand,
                                    second_strength)
                            option = 's'
                    option = '' # reset option

                    while second_strength < 21 and (option != 's' and option !=
                            'S'):
                        self.clear()
                        self.display_split_cards(first_hand, first_strength,
                                second_hand, second_strength)
                        print 'Second hand: '
                        option = raw_input('[H]it or [S]tay: ')
                        if option is 'h' or option is 'H':
                            card = self.draw_card()
                            second_hand.append(card)
                            second_strength = self.adjust_strength(second_hand)
                            self.display_split_cards(first_hand,
                                    first_strength, second_hand,
                                    second_strength)
                    option = 's'

                elif option is 'd' or option is 'D':
                    # Player wants to double
                    self.player_chips -= wager
                    wager = wager * 2
                    # Draw the player's last card
                    card = self.draw_card()
                    player_cards.append(card)
                    player_strength = self.adjust_strength(player_cards)
                    self.display_cards()
                    option = 'S' # the player will now stay

            elif (wager * 2 <= self.player_chips):
                # Player cannot split, but can double
                option = raw_input('Would you like to:\n\t[H]it' +
                       '\n\t[S]tay\n\t[D]ouble\nOption: ')
                if option is 'h' or option is 'H':
                    while player_strength <= 21 and (option != 's' and
                            option != 'S'):
                        # Player wants to hit, draw another card
                        card = self.draw_card()
                        player_cards.append(card)
                        player_strength = self.adjust_strength(player_cards)
                        self.display_cards(dealer_strength, dealer_cards,
                                player_strength, player_cards)
                        if player_strength < 21:
                            option = raw_input('[H]it or [S]tay? ')

                elif option is 'd' or option is 'D':
                    self.player_chips -= wager
                    wager = wager * 2
                    # Draw the last card for the player
                    card = self.draw_card()
                    player_cards.append(card)
                    player_strength = self.adjust_strength(player_cards)
                    self.display_cards(dealer_strength, dealer_cards,
                            player_strength, player_cards)
                    option = 's'

            else:
                # Player cannot split or double
                option = raw_input('Would you like to:\n\t[H]it' +
                        '\n\t[S]tay\nOption: ')
                if option is 'h' or option is 'H':
                    while player_strength < 21 and (option is not 's' or
                            option is not 'S'):
                        # Player wants to hit
                        card = self.draw_card()
                        player_cards.append(card)
                        player_strength = self.adjust_strength(player_cards)
                        if player_strength < 21:
                            option = raw_input('[H]it or [S]tay? ')

        self.clear()
        if len(first_hand) == 0 and len(second_hand) == 0:
            # We don't have a split
            if player_strength > 21:
                # Player is bust
                self.display_cards(dealer_strength, dealer_cards, player_strength,
                        player_cards)
                print 'You have gone bust!'
                self.lost_hands += 1
            else:
                # Reveal the dealer's hidden card
                dealer_cards.pop() # removes the '?'
                dealer_cards.append(hidden_card)
                dealer_strength = self.adjust_strength(dealer_cards)
                self.display_cards(dealer_strength, dealer_cards, player_strength,
                        player_cards)
                raw_input()
                # Now the dealer will keep drawing
                while dealer_strength < 17:
                    self.clear()
                    card = self.draw_card()
                    dealer_cards.append(card)
                    dealer_strength = self.adjust_strength(dealer_cards)
                    self.display_cards(dealer_strength, dealer_cards,
                            player_strength, player_cards)
                    raw_input()

                if not dealer_strength > 21:
                    # Dealer has not gone bust
                    if dealer_strength > player_strength:
                        print 'Dealer wins'
                        self.lost_hands += 1
                    elif dealer_strength < player_strength:
                        print 'Player wins'
                        self.won_hands += 1
                        self.player_chips += wager * 2
                    else:
                        print 'Push'
                        self.player_chips += wager
                else:
                    # Dealer's gone bust
                    print 'Player wins'
                    self.won_hands += 1
                    self.player_chips += wager * 2
        else:
            # We have a split
            if first_strength > 21 and second_strength > 21:
                # Both hands a bust
                self.display_split_cards(first_hand, first_strength,
                        second_hand, second_strength)
                print 'You have gone bust!'
                self.lost_hands += 2
            else:
                # One or no hands are bust
                # Reveal the dealer's hidden card
                dealer_cards.pop()
                dealer_cards.append(hidden_card)
                dealer_strength = self.adjust_strength(dealer_cards)
                self.display_dealer_cards(dealer_strength, dealer_cards)
                raw_input()
                # Now the dealer will keep drawing
                while dealer_strength < 17:
                    self.clear()
                    card = self.draw_card()
                    dealer_cards.append(card)
                    dealer_strength = self.adjust_strength(dealer_cards)
                    self.display_split_cards(first_hand, first_strength,
                            second_hand, second_strength)
                    self.display_dealer_cards(dealer_strength, dealer_cards)
                    raw_input()

                if not dealer_strength > 21:
                    self.display_split_cards(first_hand, first_strength,
                            second_hand, second_strength)
                    self.display_dealer_cards(dealer_strength, dealer_cards)
                    raw_input()
                    if first_strength > 21:
                        # Second hand is still ok
                        if dealer_strength > second_strength:
                            print 'Dealer wins'
                            self.lost_hands += 2
                        elif dealer_strength < second_strength:
                            print 'Second hand wins'
                            self.won_hands += 1
                            self.player_chips += wager / 2
                        else:
                            print 'Second hand push'
                        self.lost_hands += 1
                    elif second_strength > 21:
                        # First hand is still ok
                        if dealer_strength > first_strength:
                            print 'Dealer wins'
                            self.lost_hands += 2
                        elif dealer_strength < first_strength:
                            print 'First hand wins'
                            self.won_hands += 1
                            self.player_chips += wager / 2
                        else:
                            print 'Second hand push'
                            self.won_hands += 1
                        self.lost_hands += 1
                    else:
                        # Both hands aren't bust
                        if (dealer_strength > first_strength and
                                dealer_strength > second_strength):
                            print 'Dealer wins on both hands'
                            self.lost_hands += 2
                        elif (dealer_strength > first_strength and
                                dealer_strength <= second_strength):
                            print 'Hand 2 wins'
                            self.won_hands += 1
                            self.player_chips += wager / 2
                            self.lost_hands += 1
                        elif (dealer_strength <= first_strength and
                                dealer_strength > second_strength):
                            print 'Hand 1 wins'
                            self.won_hands += 1
                            self.player_chips += wager / 2
                            self.lost_hands += 1
                        else:
                            print 'Player wins'
                            self.won_hands += 2
                            self.player_chips += wager * 2
                else:
                    # Dealer is bust
                    print 'Player wins'
                    self.won_hands += 2
                    self.player_chips += wager * 2

        # Increment number of hands
        self.total_hands += 1
        print 'End of round!'

    def __init__(self, chips_start):
        """ Initialization function """
        # Set the starting chips of the player to the passed value
        self.player_chips = chips_start
        # Set the number of total hands played as well as won and lost hands
        self.total_hands = 0
        self.won_hands = 0
        self.lost_hands = 0

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

def main():
    """ Test main func for testing purposes """
    game = Game(5000)
    game.round()

if __name__ == "__main__":
    sys.exit(main())
