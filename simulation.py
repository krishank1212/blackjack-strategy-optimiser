from cards import Deck
from game import Game
from play_strategy import generate_initial_strategy
import matplotlib.pyplot as plt


# -------------------------------------------------
# Core EV evaluator (used for optimisation)
# -------------------------------------------------

def evaluate_ev(strategy, num_games=2000000, no_of_decks=6):
    """
    Pure EV evaluator.
    - Flat £1 betting only
    - No printing
    - No plotting
    - Returns EV per £ wagered
    """

    bankroll = 0.0
    total_wagered = 0.0

    deck = Deck(no_of_decks)

    for _ in range(num_games):
        if len(deck) < 52:
            deck = Deck(no_of_decks)

        game = Game(deck, strategy)
        outcomes = game.play_round()

        for outcome, bet in outcomes:
            total_wagered += bet
            bankroll += outcome * bet


    return bankroll / total_wagered


# -------------------------------------------------
# Simulation / visualisation wrapper
# -------------------------------------------------

def simulate_games(
    num_games=100_000,
    no_of_decks=6,
    betting_strategy=lambda prev, bet, limit: 1,
    plot=False,
    table_limit=None,
    strategy=None,
):
    """
    Simulation wrapper for experimentation and plotting.
    NOT used for optimisation.
    """

    wins = losses = pushes = 0
    bankroll = 0.0
    total_wagered = 0.0
    player_bj_count = dealer_bj_count = 0



    bankroll_history = []
    ev_history = []

    if strategy is None:
        strategy = generate_initial_strategy()

    deck = Deck(no_of_decks)

    for i in range(num_games):
        if len(deck) < 52:
            deck = Deck(no_of_decks)

        game = Game(deck, strategy)

        # bet = betting_strategy(prev_outcome, bet, table_limit)
        outcomes, player_blackjack, dealer_blackjack = game.play_round(True)

        if player_blackjack:
            player_bj_count += 1
        if dealer_blackjack:
            dealer_bj_count += 1



        for outcome, bet in outcomes:
            total_wagered += bet
            bankroll += outcome * bet
            if outcome > 0:
                wins += 1
            elif outcome < 0:
                losses += 1
            else:
                pushes += 1

        bankroll_history.append(bankroll)
        ev_history.append(bankroll / total_wagered)

    ev = bankroll / total_wagered

    print(f"--- Simulation Results ---")
    print(f"Rounds played: {num_games:,}")
    print(f"Wins: {wins:,}  Losses: {losses:,}  Pushes: {pushes:,}")
    print(f"Player Blackjacks: {player_bj_count}")
    print(f"Dealer Blackjacks: {dealer_bj_count}")
    print(f"Final Bankroll: £{bankroll:.2f}")
    print(f"EV per £ wagered: {ev:.4f}")

    if plot:
        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.plot(bankroll_history)
        plt.title("Bankroll Progression")
        plt.xlabel("Games")
        plt.ylabel("£")

        plt.subplot(1, 2, 2)
        plt.plot(ev_history)
        plt.axhline(0, linestyle="--")
        plt.title("EV Convergence")
        plt.xlabel("Games")
        plt.ylabel("EV")

        plt.tight_layout()
        plt.show()

    return ev
