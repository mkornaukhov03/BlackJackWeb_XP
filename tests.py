#!/usr/bin/python3
from core import *
from unittest import TestCase
import pytest


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




        
            
