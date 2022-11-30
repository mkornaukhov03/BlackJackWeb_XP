from random import randint, random
import sys
import time
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
        return self.value < num 

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
        self.game.finished = True
                

    def give_initial_cards(self): 
        self.game.dealer.add_card(self.game.deck.deal()) 
        for player in self.game.players:
            for _ in range(2):
                player.add_card(self.game.deck.deal()) 
            if player.calc_hand() == 21:
                if self.game.dealer.cards[0][0] not in ['A', 'K', 'Q', 'J']:
                    self.game.finished = True 
                    self.winner = player.id 

    def give_dealer_cards(self):
        while self.game.dealer.calc_hand() < 17:
            self.game.dealer.add_card(self.game.deck.deal())

    def finish_game(self):
        print('Game finished!')
        print(f'Winner is {self.winner}')
        print('Congratulatioins!')
            
    def run(self):
        self.game.deck.shuffle() 
        
        self.give_initial_cards() 

        if self.game.finished:
            self.finish_game()
            return
        
        for player in self.game.players: 
            value = player.calc_hand() 
            while value < 21 and self.get_answer(value): 
                player.add_card(self.game.deck.deal())  
                
        self.give_dealer_cards()
        self.check_win() 
        self.finish_game()
    


pygame.init()

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



class GuiHand(core.Deck):
    def __init__(self):
        self.cards = []
        self.card_img = []
        self.value = 0 

    def add_card(self, card):
        self.cards.append(card)
        self.display_cards()

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
            if self.value <= 10:
                self.value += 11
            else:
                self.value += 1


    def display_cards(self):
        for card in self.cards:
            cards = "".join((card[0], card[1]))
            if cards not in self.card_img:
                self.card_img.append(cards)


class GuiPlay:
    def __init__(self, name, gui_client):
        self.deck = core.Deck()
        self.dealer = GuiHand()
        self.player = GuiHand()
        self.deck.shuffle()
        self.client = gui_client
        
    def blackjack(self):

        self.dealer.calc_hand()
        self.player.calc_hand()

        self.dealer.display_cards()
        self.player.display_cards()

        show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
        
        if self.player.value == 21 and self.dealer.value == 21:
            self.client.gameDisplay.blit(show_dealer_card, (550, 200))
            self.client.black_jack("Both with BlackJack!", 500, 250, grey)
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value == 21:
            self.client.gameDisplay.blit(show_dealer_card, (550, 200))
            self.client.black_jack("You got BlackJack!", 500, 250, green)
            time.sleep(4)
            self.play_or_exit()
        elif self.dealer.value == 21:
            self.client.gameDisplay.blit(show_dealer_card, (550, 200))
            self.client.black_jack("Dealer has BlackJack!", 500, 250, red)
            time.sleep(4)
            self.play_or_exit()
            
        self.player.value = 0
        self.dealer.value = 0

    def deal(self):
        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())
        self.dealer.display_cards()
        self.player.display_cards()
        self.player_card = 1
        dealer_card = pygame.image.load('img/' + self.dealer.card_img[0] + '.png').convert()
        dealer_card_2 = pygame.image.load('img/back.png').convert()
            
        player_card = pygame.image.load('img/' + self.player.card_img[0] + '.png').convert()
        player_card_2 = pygame.image.load('img/' + self.player.card_img[1] + '.png').convert()

        
        self.client.game_texts("Dealer's hand is:", 500, 150)
        self.client.gameDisplay.blit(dealer_card, (400, 200))
        self.client.gameDisplay.blit(dealer_card_2, (550, 200))
        self.client.game_texts("Your's hand is:", 500, 400)
        self.client.gameDisplay.blit(player_card, (300, 450))
        self.client.gameDisplay.blit(player_card_2, (410, 450))
        self.blackjack()
            
            

    def hit(self):
        self.player.add_card(self.deck.deal())
        self.blackjack()
        self.player_card += 1
        
        if self.player_card == 2:
            self.player.calc_hand()
            self.player.display_cards()
            player_card_3 = pygame.image.load('img/' + self.player.card_img[2] + '.png').convert()
            self.client.gameDisplay.blit(player_card_3, (520, 450))

        if self.player_card == 3:
            self.player.calc_hand()
            self.player.display_cards()
            player_card_4 = pygame.image.load('img/' + self.player.card_img[3] + '.png').convert()
            self.client.gameDisplay.blit(player_card_4, (630, 450))
                
        if self.player.value > 21:
            show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
            self.client.gameDisplay.blit(show_dealer_card, (550, 200))
            self.client.game_finish("You Busted!", 500, 250, red)
            time.sleep(4)
            self.play_or_exit()
            
        self.player.value = 0

        if self.player_card > 4:
            sys.exit()
            
            
    def stand(self):
        self.dealer.display_cards();
        show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
        self.client.gameDisplay.blit(show_dealer_card, (550, 200))
        self.blackjack()
        self.dealer.calc_hand()
        self.player.calc_hand()
        if self.player.value > self.dealer.value:
            self.client.game_finish("You Won!", 500, 250, green)
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value < self.dealer.value:
            self.client.game_finish("Dealer Wins!", 500, 250, red)
            time.sleep(4)
            self.play_or_exit()
        else:
            self.client.game_finish("It's a Tie!", 500, 250, grey)
            time.sleep(4)
            self.play_or_exit()
        
    
    def exit(self):
        sys.exit()
    
    def play_or_exit(self):
        self.client.game_texts("Play again press Deal!", 200, 80)
        time.sleep(3)
        self.player.value = 0
        self.dealer.value = 0
        self.deck = core.Deck()
        self.dealer = GuiHand()
        self.player = GuiHand()
        self.deck.shuffle()
        self.client.gameDisplay.fill(background_color)
        pygame.draw.rect(self.client.gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
        pygame.display.update()


class GUIClient: 
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))

        pygame.display.set_caption('BlackJack')
        self.gameDisplay.fill(background_color)
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
        hand = GuiPlay(name, self)
        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    running = False

                self.button("Deal", 30, 100, 150, 50, light_slat, dark_slat, hand.deal)
                self.button("Hit", 30, 200, 150, 50, light_slat, dark_slat, hand.hit)
                self.button("Stand", 30, 300, 150, 50, light_slat, dark_slat, hand.stand)
                self.button("EXIT", 30, 500, 150, 50, light_slat, dark_red, hand.exit)
            
            pygame.display.flip()