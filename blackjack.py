from random import shuffle

class Dealer(object):
    def __init__(self):
        self.name = "Dealer"
        self.score = 0
        self.hand = []

class Player(Dealer):
    def __init__(self, name, wallet, bet=0):
        super().__init__()
        self.name = name
        self.wallet = wallet
        self.bet = bet

    @staticmethod
    def hit_or_stand():
        while True:
            choice = input("Do you want to hit? (yes/no) ")
            if choice.lower() == 'yes':
                return True
            elif choice.lower() == 'no':
                return False
            else:
                print("ERROR: Invalid Input")
                continue

    def place_bet(self, amount=5):
        self.wallet -= amount
        self.bet += amount

    def payout(self):
        self.wallet += (self.bet * 2)
        self.bet = 0

class CardDeck(object):
    #Super similar to the stack and .pop method we learned with the pringles can example.
    def __init__(self):
        self.stack = [('A', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
                      ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
                      ('J', 10), ('Q', 10), ('K', 10)] * 4
        self.shuffle()

    def shuffle(self):
        shuffle(self.stack)

    def deal_card(self):
        card = self.stack.pop()
        return card

class GamingTable(object):
    def __init__(self, player, wallet=50):
        self.dealer = Dealer()
        self.player = Player(player, wallet)
        self.deck = CardDeck()
        self.game_setup()

    def game_setup(self):
        self.deck.shuffle()
        self.player.place_bet()
        self.deal_card(self.player)
        self.deal_card(self.dealer)
        self.deal_card(self.player)
        self.calculate_score(self.player) 
        self.calculate_score(self.dealer)
        self.main()

    def main(self):
        while True:
            print()
            print(self)
            player_move = self.player.hit_or_stand()
            if player_move is True:
                self.deal_card(self.player)
                self.calculate_score(self.player)
            elif player_move is False:
                self.dealer_hit()

    def dealer_hit(self):
        score = self.dealer.score
        while True:
            if score < 17: #set to 17 as most casinos dealer stays on 17
                self.deal_card(self.dealer)
                self.calculate_score(self.dealer)
                print(self)
            elif score >= 17:
                self.check_final_score()

    def __str__(self):
        print(f'The dealers hand is {self.dealer.hand}, and their score is {self.dealer.score}')
        print('---------------------------------------------')
        print(f'{self.player.name} hand is {self.player.hand} and their score is {self.player.score}')
        print(f'Your current bank balance is {self.player.wallet}')
        print('---------------------------------------------')
        return ''

    def deal_card(self, player):
        card = self.deck.stack.pop()
        player.hand.append(card)

    def calculate_score(self, player):
        ace = False 
        score = 0
        for card in player.hand:
            if card[1] == 1 and not ace:
                ace = True
                card = ('A', 11)
            score += card[1]
        player.score = score
        if player.score > 21 and ace:
            player.score -= 10
            score = player.score
        self.check_win(score, player)
        return

    def check_win(self, score, player):
        if score > 21:
            print(f'{player.name} went over 21. Game over!')
            self.end_game()
        elif score == 21:
            print(f'{player.name} got Blackjack! Woohoo!')
            try:  
                player.payout() #pays the player if they hit blackjack. No multiplier
            except:
                pass
            self.end_game()
        else:
            return

    def check_final_score(self):
        dealer_score = self.dealer.score
        player_score = self.player.score
        if dealer_score > player_score:
            print("The Dealer/house wins!")
            self.end_game()
        else:
            print(f'{self.player.name} has won!')
            self.end_game()

    def end_game(self): #Called upon each round to end the game or continue. Or ends if money is gone.
        bank = self.player.wallet
        if bank >=10:
            again = input("Play again? (yes/no)")
            if again.lower() == 'yes':
                self.__init__(self.player.name, wallet=self.player.wallet)
            elif again.lower() == 'no':
                exit(1)
        elif bank < 10:
            print("You have ran out of money.")
            exit(2)

def main():
    player_name = input("Welcome, enter a nickname ")
    GamingTable(player_name)

if __name__ == '__main__':
    main()