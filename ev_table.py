# ev_table.py
from ev_simulation import simulate_action_from_state
from play_strategy import legal_actions

ACTIONS = ("hit", "stand", "double")

PLAYER_TOTALS = range(4, 22)          # 4–21
DEALER_UPCARDS = range(2, 12)         # 2–11 (Ace = 11)
SOFTNESS = (True, False)

def estimate_state_action_ev(
    state,
    action,
    num_samples=50_000,
    no_of_decks=6,
    strategy=None,
):
    total_profit = 0.0
    total_wager = 0.0

    for _ in range(num_samples):
        profit, wager = simulate_action_from_state(
            state,
            action,
            no_of_decks=no_of_decks,
            strategy=strategy
        )
        total_profit += profit
        total_wager += wager

    return total_profit / total_wager

def build_ev_table(
    num_samples=50_000,
    no_of_decks=6,
    strategy=None
):
    ev_table = {}

    for total in PLAYER_TOTALS:
        for is_soft in SOFTNESS:
            # Soft totals must be >= 13 (A+2)
            if total < 12 and is_soft:
                continue
            

            for dealer in DEALER_UPCARDS:
                state = (total, is_soft, dealer)
                ev_table[state] = {}

                for action in ACTIONS:

                    ev = estimate_state_action_ev(
                        state,
                        action,
                        num_samples=num_samples,
                        no_of_decks=no_of_decks,
                        strategy=strategy
                    )

                    ev_table[state][action] = ev

    return ev_table

def derive_strategy(ev_table):
    strategy = {}

    for state, action_evs in ev_table.items():
        best_action = max(action_evs, key=action_evs.get)
        strategy[state] = best_action

    return strategy

import pickle

def save_ev_table(ev_table, filename="ev_table.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(ev_table, f)

def load_ev_table(filename="ev_table.pkl"):
    with open(filename, "rb") as f:
        return pickle.load(f)