import pickle
import math
from play_strategy import always_hit_strategy
from simulation import evaluate_ev
from strategy_optimiser import mutate_strategy

# -----------------------------
# Hill-climbing optimisation
# -----------------------------

def optimise_strategy(iterations=1000, num_games=200_000, no_of_decks=6):
    """
    Optimises blackjack strategy using hill-climbing, starting from always-hit strategy.
    Returns the best strategy and a history of EVs.
    """
    
    current_strategy = always_hit_strategy()
    current_ev = evaluate_ev(current_strategy, num_games=num_games, no_of_decks=no_of_decks)
    history = [(0, current_ev)]

    print(f"Iteration 0: EV = {current_ev:.6f}")

    for i in range(1, iterations + 1):
        epsilon = 1/math.sqrt(num_games/10)  # Minimum significant improvement
        candidate_strategy = mutate_strategy(current_strategy)
        candidate_ev = evaluate_ev(candidate_strategy, num_games=int(num_games/10), no_of_decks=no_of_decks)

        if candidate_ev > current_ev + epsilon:
            epsilon = 1/math.sqrt(num_games)
            candidate_ev = evaluate_ev(candidate_strategy, num_games=num_games, no_of_decks=no_of_decks)
            if candidate_ev > current_ev + epsilon:
                current_strategy = candidate_strategy
                current_ev = candidate_ev
                history.append((i, current_ev))
                print(f"Iteration {i}: EV improved to {current_ev:.6f}")



    print(f"Optimisation complete. Best EV = {current_ev:.6f}")
    return current_strategy, history


optimal_strat, history = optimise_strategy()

# Save the best strategy
with open("best_strategy.pkl", "wb") as f:
    pickle.dump(optimal_strat, f)


