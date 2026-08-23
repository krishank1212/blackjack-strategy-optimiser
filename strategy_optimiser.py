import random

# -------------------------------------------------
# Legal actions per state (strategy-level)
# -------------------------------------------------

def legal_actions_for_state(state):
    hand_type, value, dealer = state

    if hand_type == 'pair':
        return ['hit', 'stand', 'split', 'double']

    if hand_type == 'soft':
        return ['hit', 'stand', 'double']

    # hard
    return ['hit', 'stand', 'double']


# -------------------------------------------------
# Strategy mutation
# -------------------------------------------------

def mutate_strategy(strategy):
    """
    Returns a new strategy differing at exactly one state.
    """

    new_strategy = strategy.copy()

    state = random.choice(list(strategy.keys()))
    actions = legal_actions_for_state(state)

    current_action = new_strategy[state]
    alternatives = [a for a in actions if a != current_action]

    if alternatives:
        new_strategy[state] = random.choice(alternatives)

    return new_strategy