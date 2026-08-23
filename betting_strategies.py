def martingale(prev_outcome, current_bet, table_limit=None):
    
    # Martingale betting strategy: double the bet after a loss, reset to initial bet after a win.

    if prev_outcome == 1:  # Win
        return 1  # Reset to initial bet
    elif prev_outcome == -1 and (table_limit is None or (current_bet * 2 <= table_limit)): # Loss
        return current_bet * 2 
    else:  # Push
        return current_bet
    
def hi_lo():
    pass