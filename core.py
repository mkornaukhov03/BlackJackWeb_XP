import random


SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for value in RANKS:
            for suit in SUITS:
                self.cards.append((value, suit))
  
    def shuffle(self):
        random.shuffle(self.cards)
        

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop()

class Hand: 
    def __init__(self, id : str):
        self.cards = []
        self.value = 0 
        self.id = id

    def add_card(self, card):
        self.cards.append(card)

    def calc_hand(self):
        first_card_index = [a_card[0] for a_card in self.cards]
        non_aces = [c for c in first_card_index if c != 'A']
        aces = [c for c in first_card_index if c == 'A']

        for card in non_aces:
            if card in 'JQK':
                self.value += 10
            else:
                self.value += int(card)

        for card in aces:
            if self.value <= 21:
                self.value += 11
            else:
                self.value += 1

# dealer only 
class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.build()
        self.dealer = Hand()
        self.players = []
    def register(self, h : Hand):
        self.players.append(h)


class CLI:
    def __init__(self, num_of_players : int):
        self.num_of_players = num_of_players
        self.game = Game()
        # for 1 player 
    
    def add_player(self, id : str):
        self.game.register(Hand(id))
        
    def run(self):
        pass
    

