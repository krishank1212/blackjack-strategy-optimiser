import pickle
import math
from play_strategy import always_hit_strategy, generate_initial_strategy
from simulation import evaluate_ev
from strategy_optimiser import mutate_strategy
from matplotlib import pyplot as plt

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

def compare_strategy():
    """
    Compares the number of state matches between true basic strategy and the optimised strategy. 
    Analyses whether the remaining gap was because states were never mutated from the always hit, or mutated incorrectly.
    """
    with open("best_strategy.pkl", "rb") as f:
        optimised_strategy = pickle.load(f)
    basic_strategy = generate_initial_strategy()
    seed_strategy = always_hit_strategy()
    state_count = len(basic_strategy)
    match_count = 0
    bad_mutation_count = 0
    no_mutation_count = 0
    luck_count = 0
    for state in basic_strategy:
        if state in optimised_strategy and optimised_strategy[state] == basic_strategy[state]:
            match_count += 1
            if state in optimised_strategy and seed_strategy[state] == optimised_strategy[state]:
                luck_count += 1
        elif state in seed_strategy and optimised_strategy[state] == seed_strategy[state]:
            no_mutation_count += 1
        elif state in optimised_strategy and optimised_strategy[state] != basic_strategy[state]:
            bad_mutation_count += 1
        
        
    
    return state_count, match_count, bad_mutation_count, no_mutation_count, luck_count
   
state_count, match_count, bad_mutation_count, no_mutation_count, luck_count = compare_strategy()
print(f"Total states: {state_count}")
print(f"Matching states: {match_count}")
print(f"Badly mutated states: {bad_mutation_count}")
print(f"Unmutated states: {no_mutation_count}")
print(f"States that remained 'hit': {luck_count}")

iterations, evs = zip(*history)
plt.step(iterations, evs, where='post')
plt.xlabel("Iteration")
plt.ylabel("EV per £ wagered")
plt.title("Hill-climbing convergence")
plt.show()
