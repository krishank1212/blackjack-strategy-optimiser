# play_strategy.py

# -----------------------------
# State Encoding
# -----------------------------

def encode_state(player_hand, dealer_upcard):
    """
    Encodes the blackjack decision state as a tuple.

    State format:
        (hand_type, player_value, dealer_upcard)

    hand_type:
        'hard', 'soft', or 'pair'

    player_value:
        - hard / soft: total hand value
        - pair: rank of the pair ('2'–'10', 'A')

    dealer_upcard:
        2–11 (Ace = 11)
    """

    dealer_value = dealer_upcard.value

    # # Pair
    # if (
    #     len(player_hand.cards) == 2
    #     and player_hand.cards[0].rank == player_hand.cards[1].rank
    # ):
    #     return ("pair", player_hand.cards[0].rank, dealer_value)

    # # Soft
    # if player_hand.is_soft():
    #     return ("soft", player_hand.value, dealer_value)

    # # Hard
    # return ("hard", player_hand.value, dealer_value)
    
    return (player_hand.value, player_hand.is_soft(), dealer_value)


# -----------------------------
# Strategy Policy (lookup only)
# -----------------------------

def strategy_policy(player_hand, dealer_upcard, strategy):
    """
    Given a strategy dictionary, returns the action for the current state.

    strategy:
        dict mapping state -> action

    action:
        'hit', 'stand', 'double', 'split'
    """

    state = encode_state(player_hand, dealer_upcard)

    if state not in strategy:
        raise KeyError(f"State {state} not found in strategy.")

    return strategy[state]


# -----------------------------
# Legal Action Constraints
# -----------------------------

def legal_actions(player_hand):
    """
    Returns the list of legal actions for the given hand.
    Enforces blackjack rules independently of strategy.
    """

    actions = ['hit']
    
    if player_hand.value >= 12:
        actions.append('stand')

    # Double only allowed on first move
    if len(player_hand.cards) == 2:
        actions.append('double')

        # Split only if pair
        if player_hand.cards[0].rank == player_hand.cards[1].rank:
            actions.append('split')

    return actions


# -----------------------------
# Initial Strategy Generator
# -----------------------------

# def generate_initial_strategy():
    """
    Generates a reasonable starting strategy (basic-strategy-like)
    without hard-coding logic into the game engine.

    This strategy is intended ONLY as a starting point for optimisation.
    """

    # strategy = {}

    # dealer_upcards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # # -----------------
    # # Hard totals
    # # -----------------
    # for dealer in dealer_upcards:
    #     for total in range(5, 22):

    #         if total >= 17:
    #             action = 'stand'
    #         elif total <= 8:
    #             action = 'hit'
    #         elif total == 9:
    #             action = 'double' if 3 <= dealer <= 6 else 'hit'
    #         elif total == 10:
    #             action = 'double' if dealer <= 9 else 'hit'
    #         elif total == 11:
    #             action = 'double'
    #         elif total == 12:
    #             action = 'stand' if 4 <= dealer <= 6 else 'hit'
    #         else:  # 13–16
    #             action = 'stand' if 2 <= dealer <= 6 else 'hit'

    #         strategy[('hard', total, dealer)] = action

    # # -----------------
    # # Soft totals
    # # -----------------
    # for dealer in dealer_upcards:
    #     for total in range(13, 22):

    #         if total <= 17:
    #             action = 'double' if 4 <= dealer <= 6 else 'hit'
    #         elif total == 18:
    #             if dealer in (3, 4, 5, 6):
    #                 action = 'double'
    #             elif dealer in (2, 7, 8):
    #                 action = 'stand'
    #             else:
    #                 action = 'hit'
    #         else:  # 19–21
    #             action = 'stand'

    #         strategy[('soft', total, dealer)] = action

    # # -----------------
    # # Pairs
    # # -----------------
    # pair_ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

    # for dealer in dealer_upcards:
    #     for rank in pair_ranks:

    #         if rank in ('A', '8'):
    #             action = 'split'
    #         elif rank in ('10','J','Q','K'):
    #             action = 'stand'
    #         elif rank == '9':
    #             action = 'split' if dealer in (2,3,4,5,6,8,9) else 'stand'
    #         elif rank == '7':
    #             action = 'split' if dealer <= 7 else 'hit'
    #         elif rank == '6':
    #             action = 'split' if dealer <= 6 else 'hit'
    #         elif rank == '5':
    #             action = 'double' if dealer <= 9 else 'hit'
    #         elif rank == '4':
    #             action = 'split' if dealer in (5,6) else 'hit'
    #         else:  # 2s and 3s
    #             action = 'split' if dealer <= 7 else 'hit'

    #         strategy[('pair', rank, dealer)] = action

    # return strategy
def generate_initial_strategy():
    strategy = {}

    for total in range(4, 22):
        for is_soft in (True, False):
            for dealer in range(2, 12):
                state = (total, is_soft, dealer)

                # Fill with your baseline logic
                if is_soft:
                    if total <= 13:
                        action = 'hit'
                    elif total <= 17:
                        action = 'double' if 4 <= dealer <= 6 else 'hit'
                    elif total == 18:
                        if dealer in (3, 4, 5, 6):
                            action = 'double'
                        elif dealer in (2, 7, 8):
                            action = 'stand'
                        else:
                            action = 'hit'
                    else:  # 19–21
                        action = 'stand'
                else:
                    if total >= 17:
                        action = 'stand'
                    elif total <= 8:
                        action = 'hit'
                    elif total == 9:
                        action = 'double' if 3 <= dealer <= 6 else 'hit'
                    elif total == 10:
                        action = 'double' if dealer <= 9 else 'hit'
                    elif total == 11:
                        action = 'double'
                    elif total == 12:
                        action = 'stand' if 4 <= dealer <= 6 else 'hit'
                    else:  # 13–16
                        action = 'stand' if 2 <= dealer <= 6 else 'hit'
                strategy[state] = action

    return strategy