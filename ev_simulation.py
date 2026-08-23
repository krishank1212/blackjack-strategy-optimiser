def simulate_action_from_state(state, action, no_of_decks=6, strategy=None):
    from cards import Deck, Card
    from hand import Hand
    from play_strategy import generate_initial_strategy

    if strategy is None:
        strategy = generate_initial_strategy()

    player_total, is_soft, dealer_upcard = state

    deck = Deck(no_of_decks)
    deck.shuffle()

    player_hand = construct_player_hand(player_total, is_soft)

    dealer_hand = Hand()
    dealer_hand.add_card(Card('A' if dealer_upcard == 11 else str(dealer_upcard), dealer_upcard))
    dealer_hand.add_card(deck.draw_card())

    bet = 1

    # Forced action
    if action == "hit":
        player_hand.add_card(deck.draw_card())
    elif action == "double":
        bet = 2
        player_hand.add_card(deck.draw_card())

    # Finish player hand
    if action != "double":
        while not player_hand.is_bust():
            key = (player_hand.value, player_hand.is_soft(), dealer_upcard)
            if strategy[key] == "hit":
                player_hand.add_card(deck.draw_card())
            else:
                break

    # Dealer play
    while dealer_hand.value < 17 or (
        dealer_hand.value == 17 and dealer_hand.is_soft()
    ):
        dealer_hand.add_card(deck.draw_card())

    # Resolve
    if player_hand.is_bust():
        return (-bet, bet)
    elif dealer_hand.is_bust():
        return (bet, bet)
    elif player_hand.value > dealer_hand.value:
        return (bet, bet)
    elif player_hand.value < dealer_hand.value:
        return (-bet, bet)
    else:
        return (0, bet)
    

def construct_player_hand(total, is_soft):
    from hand import Hand
    from cards import Card
    hand = Hand()

    if is_soft:
        # Must include an Ace counted as 11
        hand.add_card(Card('A', 11))
        hand.add_card(Card(str(total - 11), total - 11))
    else:
        hand.add_card(Card(str(total // 2), total // 2))
        hand.add_card(Card(str(total - total // 2), total - total // 2))

    return hand