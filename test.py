#testing for cards.py and hand.py
# from cards import Deck
# from hand import Hand

# deck = Deck()
# player = Hand()
# deck.shuffle()
# player.add_card(deck.draw_card())
# player.add_card(deck.draw_card())

# print(player)  # Shows cards and value
# print("Is Blackjack?", player.is_blackjack()) #True for cases when total is 21.
# print("Is Bust?", player.is_bust())#Always false since you can't bust with only two cards, but ensures that if the player has a blackjack, they haven't also busted (boundary check).
# print("Is Soft?", player.is_soft())  # True if the hand contains an Ace. If is_blackjack is true, this will also be true since a blackjack is always soft.

#testing for strategy.py
# from cards import Deck
# from hand import Hand
# from strategy import basic_startegy
# deck = Deck()
# deck.shuffle()
# player_hand = Hand()
# player_hand.add_card(deck.draw_card())
# player_hand.add_card(deck.draw_card())
# dealer_upcard = deck.draw_card()
# print("Player's Hand:", player_hand)
# print("Dealer's Upcard:", dealer_upcard)
# action = basic_startegy(player_hand, dealer_upcard)
# print(action) # Expected output: 'hit', 'stand' or 'double' based on the player's hand and dealer's upcard.

#testing for game.py
# from game import Game
# from cards import Deck
# def main():
#     score = 0
#     deck = Deck(6)
#     for i in range(5):
#         game = Game(deck)
#         outcome = game.play_round()
#         print(f"Round outcome: {outcome}")  # 1 for player win, -1 for dealer win, 0 for tie
#         score += outcome
#     print(f"Final Score after 5 rounds: {score}")

# if __name__ == "__main__":
#     main()

#testing for simulation.py
# from simulation import simulate_games
# if __name__ == "__main__":
#     simulate_games(1000000, 4)
    
"""Results set 1 (6 decks):
--- Simulation Results ---
Rounds played: 10,000
Wins: 4,330  Losses: 4,697  Pushes: 973
Win rate: 43.30%, Loss rate: 46.97%, Push rate: 9.73%
EV per hand (assuming $1 bet): -0.0367

Results set 2 (8 decks):
--- Simulation Results ---
Rounds played: 100,000
Wins: 42,527  Losses: 48,241  Pushes: 9,232
Win rate: 42.53%, Loss rate: 48.24%, Push rate: 9.23%
EV per hand (assuming $1 bet): -0.0571

Results set 3 (4 decks):
Rounds played: 1,000,000
Wins: 429,553  Losses: 477,947  Pushes: 92,500
Win rate: 42.96%, Loss rate: 47.79%, Push rate: 9.25%
EV per hand (assuming $1 bet): -0.0484"""
    
# from play_strategy import generate_initial_strategy
# from simulation import evaluate_ev
# from strategy_optimiser import mutate_strategy

# s = generate_initial_strategy()
# ev = evaluate_ev(s)

# s2 = mutate_strategy(s)
# ev2 = evaluate_ev(s2)

# print(ev, ev2)

# from simulation import evaluate_ev
# from pickle import load

# with open("best_strategy.pkl", "rb") as f:
#     best_strategy = load(f)

# print(evaluate_ev(best_strategy, num_games=1_000_000))

# build_ev_table_runner.py
from ev_table import build_ev_table, save_ev_table, load_ev_table, derive_strategy
from simulation import evaluate_ev
from play_strategy import generate_initial_strategy
ev_table = build_ev_table(num_samples=20_000)
save_ev_table(ev_table)
baseline_strategy = generate_initial_strategy()
ev_table = load_ev_table("ev_table.pkl")

derived_strategy = derive_strategy(ev_table)
print(ev_table[(4, False, 2)])
print(baseline_strategy[(4, False, 2)])
print(derived_strategy[(4, False, 2)])
baseline_ev = evaluate_ev(baseline_strategy, num_games=1000000, no_of_decks=6)
derived_ev = evaluate_ev(derived_strategy, num_games=1000000, no_of_decks=6)
print("Baseline strategy EV:", round(baseline_ev, 5))
print("EV-derived strategy EV:", round(derived_ev, 5))
print("Delta EV:", round(derived_ev - baseline_ev, 5))