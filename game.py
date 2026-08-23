from hand import Hand
from play_strategy import strategy_policy, legal_actions

class Game:
    def __init__(self, deck, strategy):
        self.deck = deck
        self.strategy = strategy
        self.player_hands = [(Hand(), 1)]
        self.dealer_hand = Hand()


    def deal_initial_cards(self):
        for hand in self.player_hands:
            hand[0].add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())
        for hand in self.player_hands:
            hand[0].add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())

    def play_round(self, return_blackjack_flags=False):
        results = []
        self.deal_initial_cards()
        dealer_upcard = self.dealer_hand.cards[0]
        
        player_blackjack = self.player_hands[0][0].is_blackjack()
        dealer_blackjack = self.dealer_hand.is_blackjack()

        # Check for immediate blackjack outcomes
        if player_blackjack or dealer_blackjack:
            if player_blackjack and not dealer_blackjack:
                result = 1.5
            elif dealer_blackjack and not player_blackjack:
                result = -1
            else:
                result = 0  # both have blackjack = push
            
            results.append((result, 1))

            return (results, player_blackjack, dealer_blackjack) if return_blackjack_flags else results

        i = 0
        while i < len(self.player_hands):
            hand, bet = self.player_hands[i]


            while True:
                action = strategy_policy(hand, dealer_upcard, self.strategy)

                # enforce legal actions
                legal = legal_actions(hand)
                if action not in legal:
                    action = 'hit'

                if action == 'stand':
                    break

                elif action == 'split':
                    new_hand = Hand()
                    new_hand.add_card(hand.cards.pop())
                    hand.add_card(self.deck.draw_card())
                    new_hand.add_card(self.deck.draw_card())
                    self.player_hands[i] = (hand, bet)
                    self.player_hands.append((new_hand, bet))
                    # do not increment i yet; will process current hand again if needed
                    continue  # re-evaluate current hand after split

                elif action == 'hit':
                    hand.add_card(self.deck.draw_card())
                    
                elif action == 'double':
                    hand.add_card(self.deck.draw_card())
                    bet *= 2
                    if hand.is_bust():
                        results.append((-1, bet))
                    break

                if hand.is_bust():
                    results.append((-1, bet))
                    break

            i += 1

        # Dealer's turn given the player hasn't busted. If the player has busted the dealer doesn't play.
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.draw_card())
        
        for hand, bet in self.player_hands:
            if hand.is_bust():
                continue
            elif (self.dealer_hand.is_bust() or hand.value > self.dealer_hand.value):
                result = 1
            elif hand.value < self.dealer_hand.value:
                result = -1
            else:
                result = 0
            
            results.append((result, bet))
        
        return (results, player_blackjack, dealer_blackjack) if return_blackjack_flags else results