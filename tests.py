#!/usr/bin/python3
from core import *
from unittest import TestCase
import pytest
from clients import CLI


# Test core
class TryTesting(TestCase):
    def test_deck_build(self):
        d = Deck()
        self.assertEqual(len(d.cards), len(SUITS) * len(RANKS))

    def test_deck_shuffle(self):
        d = Deck()
        prev = d.cards.copy()
        d.shuffle()
        self.assertNotEqual(prev, d.cards)
    
    def test_deck_deal(self):
        d = Deck()
        
        d.deal()

        d.shuffle()
        self.assertEqual(len(d.cards) + 1, len(SUITS) * len(RANKS))
    
    def test_hand_init(self):
        hands = [Hand(str(h)) for h in range(100)]
        for i, h in enumerate(hands):
            self.assertTrue(h.id == str(i))
    
    def test_hand_add_card(self):
        h = Hand("abobus")
        d = Deck()
        cards = [d.deal() for _ in range(20)]
        for c in cards:
            h.add_card(c)
        
        self.assertEqual(set(cards), set(h.cards))
    
    def test_hand_calc(self):
        h = Hand("abobus")
        d = Deck()
        cards = [('C', '2'), ('D', '3'), ('S', '4')]
        for (i, j) in cards:
            h.add_card((j, i))
        h.calc_hand()
        self.assertEqual(h.value, 9)
        
    def test_game(self):
        g = Game()
        h = Hand("kek")
        g.register(h)
        self.assertEqual(h, g.players[0])

# test CLI

class TryTesting(TestCase):
    def cli_greedy_win_test(self):
        cli = CLI(1, kind=15)
        cli.add_player("Andrei")
        hacked_deck = Deck()
        hacked_deck.cards = [("2", "C"), ("A", "C"), ("10", "C")]
        cli.game.deck = hacked_deck
        cli.run()
        self.assertTrue(cli.winner == "Andrei")

    def cli_greedy_lose_test(self):
        cli = CLI(1, kind=22)
        cli.add_player("Andrei")
        hacked_deck = Deck()
        hacked_deck.cards = [("2", "C"), ("A", "C"), ("10", "C"), ("9", "D")] 
        cli.game.deck = hacked_deck 
        cli.run() 
        self.assertTrue(cli.winner == "Dealer")

    def cli_draw_test(self):
        cli = CLI(1, kind=21)
        cli.add_player("Andrei")
        hacked_deck = Deck()
        hacked_deck.cards = [("10", "C"), ("A", "C"), ("10", "C"), ("A", "D")] 
        cli.game.deck = hacked_deck 
        cli.run()
        self.assertEqual(cli.winner, "Draw") 

    





        
            
