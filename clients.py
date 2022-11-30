from random import randint, random
import sys
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
            return random.randrange(0, 2) == 0

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
                
    

CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
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
font = pygame.font.SysFont("Arial", 20)
textfont = pygame.font.SysFont('Comic Sans MS', 35)
game_end = pygame.font.SysFont('dejavusans', 100)
blackjack = pygame.font.SysFont('roboto', 70)



class GuiHand(core.Hand):
    def __init__(self, name : str):
        self.super().__init__(name)

    def blackjack(self):
        pass

    def deal(self):
        pass

    def hit(self):
        pass

    def stand(self):
        pass

    def end_game(self):
        sys.exit()
    
    def play_or_exit(self):
        pass

class GUIClient: 
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))

        pygame.init()

        pygame.display.set_caption('BlackJack')
        self.gameDisplay.fill(self.background_color)
        pygame.draw.rect(self.gameDisplay, grey, pygame.Rect(0, 0, 250, 700))

    def text_objects(self, text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    def end_text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()


    #game text display
    def game_texts(self, text, x, y):
        TextSurf, TextRect = self.text_objects(text, textfont)
        TextRect.center = (x, y)
        self.gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()

    
    def game_finish(self, text, x, y, color):
        TextSurf, TextRect = self.end_text_objects(text, game_end, color)
        TextRect.center = (x, y)
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()

    def black_jack(self, text, x, y, color):
        TextSurf, TextRect = self.end_text_objects(text, blackjack, color)
        TextRect.center = (x, y)
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        
    #button display
    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, ac, (x, y, w, h))
            if click[0] == 1 != None:
                action()
        else:
            pygame.draw.rect(self.gameDisplay, ic, (x, y, w, h))

        TextSurf, TextRect = self.text_objects(msg, font)
        TextRect.center = ((x + (w/2)), (y + (h/2)))
        self.gameDisplay.blit(TextSurf, TextRect)


    def run(self, name : str):
        running = True
        hand = (name)
        while running:
            for event in pygame.event.get():
                if event.kind == pygame.QUIT:
                    running = False

                self.button("Deal", 30, 100, 150, 50, light_slat, dark_slat, play_blackjack.deal)
                self.button("Hit", 30, 200, 150, 50, light_slat, dark_slat, play_blackjack.hit)
                self.button("Stand", 30, 300, 150, 50, light_slat, dark_slat, play_blackjack.stand)
                self.button("EXIT", 30, 500, 150, 50, light_slat, dark_red, play_blackjack.exit)
            
        pygame.display.flip()