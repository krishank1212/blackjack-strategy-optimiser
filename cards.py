import random

class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __repr__(self):
        return f"Card({self.suit}, {self.rank})"
    
    @property
    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank) 
        
class Deck:
    def __init__(self, no_of_decks=1):
        self.no_of_decks = no_of_decks
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS] * no_of_decks
        self.shuffle() # Shuffle the deck upon initialisation
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def draw_card(self):
        if not self.cards:
            self.__init__(self.no_of_decks)  # Reinitialise the deck if empty
        return self.cards.pop()
    
    def __len__(self):
        return len(self.cards)



