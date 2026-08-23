class Hand:
    def __init__(self):
        self.cards = []
        self.aces = 0
    def add_card(self, card):
        self.cards.append(card)
        
    @property    
    def value(self):
        val = sum(card.value for card in self.cards)
        self.aces = sum(1 for card in self.cards if card.rank == 'A')
        while val > 21 and self.aces:
            val -= 10
            self.aces -= 1
        return val
    
    def is_blackjack(self):
        return len(self.cards) == 2 and self.value == 21
    
    def is_bust(self):
        return self.value > 21
    
    def __repr__(self):
        return f"Hand({self.cards}) --> {self.value})"
    
    def is_soft(self):
        return self.value <= 21 and self.aces > 0
    
