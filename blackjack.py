import random
from random import shuffle


class Player:
    def __init__(self, name):
        self.name = name
        self.bankroll = 1000
        self.bet = 0
        self.current_hand = []

    def make_an_ace_one(self):
        count = 0
        for i in self.current_hand:
            if self.current_hand[count].worth == 11:
                self.current_hand[count].worth = 1
                break
            count += 1


class Dealer:
    def __init__(self):
        self.name = "Dealer"
        self.bankroll = 100000
        self.current_hand = []

    def make_an_ace_one(self):
        count = 0
        for i in self.current_hand:
            if self.current_hand[count].worth == 11:
                self.current_hand[count].worth = 1
                break
            count += 1


class Card:
    suits = ["clubs", "hearts", "diamonds", "spades"]
    values = [None, None, 2, 3, 4, 5, 6, 7, 8,
              9, 10, "Jack", "Queen", "King", "Ace"]

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

        # this shit was wrong
        # if self.value == 11 or 12 or 13:
        if self.value in [11, 12, 13]:
            self.worth = 10

        elif self.value == 14:
            self.worth = 11

        else:
            self.worth = self.value

    def __repr__(card):
        return f"{card.values[card.value]} of {card.suits[card.suit]}"


class Deck:
    deck = []

    def __init__(self):
        for i in range(2, 15):
            for j in range(0, 4):
                self.deck.append(Card(i, j))
        random.shuffle(self.deck)

    # def print_deck(self):
    #     a = 0
    #     for i in self.deck:
    #         print(self.deck[a])
    #         a += 1


class Game:
    def __init__(self):
        self.dealer = Dealer()
        self.deck = Deck()
        print("Welcome to Blackjack! ")
        done = False
        while True:
            try:
                self.player1 = Player(input("enter player's name: "))
                done = True
            except:
                print("try again")
            if done:
                break

    def point_counter(self, player):
        sum = 0
        j = 0
        for i in player.current_hand:
            sum = sum + player.current_hand[j].worth
            j = j + 1
        return sum

    def bet(self):
        betting_done = False
        while betting_done == False:
            print(
                f"{self.player1.name}, how much do you want to bet? (you have {self.player1.bankroll}$)")
            self.player1.bet = int(input("enter bet amount: "))
            if self.player1.bankroll >= self.player1.bet and self.player1.bet > 0:
                self.player1.bankroll = self.player1.bankroll - self.player1.bet
                betting_done = True
            else:
                print("you don't have that much money!")
                pass

    def deal(self):

        if len(self.deck.deck) < 16:
            print("***the deck has been reset!")
            deck = Deck()

        print("the dealer starts dealing the cards")
        # "deck" is an instance of the Deck object and the second "deck" is a list in that object
        self.player1.current_hand.append(self.deck.deck.pop())
        self.dealer.current_hand.append(self.deck.deck.pop())
        print(f"{self.dealer.name} has {self.dealer.current_hand}")
        self.player1.current_hand.append(self.deck.deck.pop())
        self.dealer.current_hand.append(self.deck.deck.pop())

        if self.point_counter(self.player1) > 21:
            Player.make_an_ace_one(self.player1)

        print(f"{self.player1.name} has {self.player1.current_hand}")
        # calculating the points of a hand with the function
        print(f"your hand is {self.point_counter(self.player1)} points")
        check_for_blackjack = False
        # if the player gets 21
        if self.player1.current_hand[0].worth + self.player1.current_hand[1].worth == 21:
            win = self.player1.bet*3/2
            self.player1.bankroll += self.player1.bet*1.5
            print(f"blackjack! you win{self.player1.bet*1.5}$!")
            self.player1.current_hand = []
            self.dealer.current_hand = []
            return False  # resets round
        return True

    def hit_or_stand(self):
        while True:

            bust = False

            answer = input(
                "press \"h\" if you want to hit or \"s\" if you want to stand: ")

            if answer.lower() == "h":
                self.player1.current_hand.append(self.deck.deck.pop())
                Player.make_an_ace_one(self.player1)

                if self.point_counter(self.player1) > 21:
                    Player.make_an_ace_one(self.player1)

                print(f"your cards are {self.player1.current_hand}")
                print(
                    f"your hand is {self.point_counter(self.player1)} points")
                if self.point_counter(self.player1) > 21:
                    print(f"you bust! you lose {self.player1.bet}$! ")
                    bust = True
                    break

            elif answer.lower() == "s":
                print(
                    f"you exit with {self.point_counter(self.player1)} points! now is the dealers turn. ")
                return True  # so that the if statement in the begin_game() proceeds with dealers turn

            else:
                print("incorrect input ")
                continue

            if bust == True:
                self.player1.current_hand = []
                self.dealer.current_hand = []
                continue

    def dealers_turn(self):
        while True:
            print(
                f"the dealers hand: {self.dealer.current_hand}, {self.point_counter(self.dealer)}")
            # check for black jack and decide win or push
            if self.point_counter(self.dealer) == 21:

                if self.check_for_blackjack:
                    print(
                        f"{self.player1.name} and dealer both have blackjack! it's a push. your bet is returned")
                    self.player1.bankroll += self.player1.bet
                    break

                else:
                    print("dealer hit blackjack! you lose your bet")
                    break

            # hit or stand
            # when to hit or stand and decide win lose
            # if point_counter(self.player1) == 21 and point_counter(self.dealer) == 21, decide push
            while True:
                Dealer.make_an_ace_one(self.dealer)
                if self.point_counter(self.dealer) <= 16:
                    self.dealer.current_hand.append(self.deck.deck.pop())
                    print(
                        f"the dealers hand: {self.dealer.current_hand}, {self.point_counter(self.dealer)} points")
                    pass

                elif self.point_counter(self.dealer) >= 17:
                    break

            # deciding winner or draw
            if self.point_counter(self.dealer) == 21 and self.point_counter(self.player1) == 21:
                print("it's a push! your bet is retuened. ")
                break

            elif self.point_counter(self.dealer) > 21:
                print("the dealer busted! you win!")
                self.player1.bankroll += (self.player1.bet*2)
                break
            elif self.point_counter(self.dealer) > self.point_counter(self.player1):
                print(f"you lose your bet! ({self.player1.bet})")
                self.dealer.bankroll += self.player1.bet
                break

            elif self.point_counter(self.dealer) < self.point_counter(self.player1):
                print(f"you win! +{self.player1.bet*2}$")
                self.player1.bankroll += (self.player1.bet*2)
                break

            elif self.point_counter(self.dealer) == self.point_counter(self.player1):
                print(f"it's a push! your {self.player.bet}$ is returned")
                self.player1.bankroll += self.player1.bet
                break

            else:
                print("***just cheking if i messed up somewhere")

            break
        self.player1.current_hand = []
        self.dealer.current_hand = []

    def begin_game(self):

        while True:

            b = False
            self.bet()
            a = self.deal()

            if a:
                b = self.hit_or_stand()
            if b:
                self.dealers_turn()

            self.player1.current_hand = []
            self.dealer.current_hand = []


if __name__ == "__main__":

    game = Game()
    game.begin_game()
