from random import randint, random
import core

import pygame


class CLI:
    def __init__(self, num_of_players : int, kind):
        self.num_of_players = num_of_players
        self.game = core.Game()
        self.winner = None
        self.kind = kind 
        # for 1 player 

        # kind is 'input' or 'random' or num for greedy
    
    def greedy_answer(self, num):
        return self.value < num;

    def add_player(self, id : str):
        self.game.register(core.Hand(id))

    def get_answer(self, cur_value: int):
        if str(self.kind) == 'input':
            answer = input('kind hit to add card or stop to stop')
            return answer == 'hit'

        elif str(self.kind) == 'random':
            return random.randrange(0, 2)

        else: 
            return cur_value < self.kind 

    # after all cards given
    def check_win(self):
        dealer_value = self.game.dealer.calc_hand()
        for player in self.game.players:
            player_value = player.calc_hand() 
            if dealer_value == 21: 
                if player_value != 21: 
                    self.winner = self.game.dealer.id 
                else:
                    self.winner = 'draw'  
            elif player_value == 21:
                self.winner = player.id 
            elif player_value < 21 and dealer_value < 21:
                if player_value < dealer_value:
                    self.winner = self.game.dealer.id 
                elif player_value > dealer_value:
                    self.winner = player.id
                else:
                    self.winner = 'draw'
            else:
                self.winner = 'draw'
                

    def give_initial_cards(self): 
        self.game.dealer.add_card(self.game.deck.deal()) 
        for player in self.game.players:
            for _ in range(2):
                player.add_card(self.game.deck.deal()) 
            if player.calc_hand() == 21:
                if self.game.dealer.cards[0][0] not in ['A', 'K', 'Q', 'J']:
                    self.game.finished = True 
                    self.winner = player.id 
            
    def run(self):
        self.game.deck.shuffle() 
        
        self.give_initial_cards() 
        
        for player in self.game.players: 
            value = player.calc_hand() 
            while value < 21 and self.get_answer(value): 
                player.add_card(self.game.deck.deal())  
                
    
class GUIClient: 
    def __init__(self):
        display_width = 900
        display_height = 700
        background_color = (34,139,34)
        grey = (220,220,220)
        black = (0,0,0)
        green = (0, 200, 0)
        red = (255,0,0)
        light_slat = (119,136,153)
        dark_slat = (47, 79, 79)
        dark_red = (255, 0, 0)
        pygame.init()
        font = pygame.font.SysFont("Arial", 20)
        textfont = pygame.font.SysFont('Comic Sans MS', 35)
        game_end = pygame.font.SysFont('dejavusans', 100)
        blackjack = pygame.font.SysFont('roboto', 70)

        clock = pygame.time.Clock()

        gameDisplay = pygame.display.set_mode((display_width, display_height))

        pygame.display.set_caption('BlackJack')
        gameDisplay.fill(background_color)
        pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))