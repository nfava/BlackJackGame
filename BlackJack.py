import random

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
MIN_BET = 5
START_BANKROLL = 100


def create_deck():
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck

def card_value(card):
    rank, _ = card
    if rank in ["J", "Q", "K"]:
        return 10
    if rank == "A":
        return 11
    return int(rank)

def hand_value(hand):
    total = sum(card_value(card) for card in hand)
    aces = sum(1 for card in hand if card[0] == 'A')

    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21

def card_str(card):
    return f"{card[0]} of {card[1]}"

def display_hand(hand, who="Player", hide_first=False):
    if hide_first:
        print(f"{who}'s hand: [hidden], {card_str(hand[1])}")
    else:
        print(f"{who}'s hand: {', '.join(card_str(c) for c in hand)} "
              f"(Value: {hand_value(hand)})")

def take_bet(bankroll):
    while True:
        try:
            bet = int(input(f"Place your bet (min ${MIN_BET}, bankroll ${bankroll}): $"))
            if bet < MIN_BET:
                print(f"Minimum bet is ${MIN_BET}.")
            elif bet > bankroll:
                print("You can't bet more than your bankroll.")
            else:
                return bet
        except ValueError:
            print("Enter a valid number.")

def player_turn(deck, hand, bankroll, bet):
    first_turn = True
    while True:
        display_hand(hand, "Player")

        if hand_value(hand) > 21:
            print("You busted!")
            return hand, bet, True
        # Options
        options = ["(H)it", "(S)tand"]
        if first_turn and bankroll >= bet:
            options.append("(D)ouble Down")
        choice = input(f"Choose {', '.join(options)}: ").strip().lower()
        if choice.startswith("h"):
            hand.append(deck.pop())
        elif choice.startswith("s"):
            return hand, bet, False
        elif choice.startswith("d") and first_turn:
            # Double bet, draw one card, then stand
            bet *= 2
            hand.append(deck.pop())
            display_hand(hand, "Player")
            if hand_value(hand) > 21:
                print("You busted after doubling!")
                return hand, bet, True
            return hand, bet, False
        else:
            print("Invalid choice.")
            continue

        first_turn = False

def dealer_turn(deck, hand):
    while hand_value(hand) < 17:
        hand.append(deck.pop())
    display_hand(hand, "Dealer")
    return hand, hand_value(hand) > 21

def settle_bet(player_hand, dealer_hand, bet):
    p_val = hand_value(player_hand)
    d_val = hand_value(dealer_hand)


    if is_blackjack(player_hand) and not is_blackjack(dealer_hand):
        win = int(bet * 1.5)
        print(f"Blackjack! You win ${win}")
        return win
    if is_blackjack(dealer_hand) and not is_blackjack(player_hand):
        print("Dealer has blackjack. You lose.")
        return -bet
    if p_val > 21:
        print("You busted!")
        return -bet
    if d_val > 21:
        print("Dealer busted! You win!")
        return bet
    if p_val > d_val:
        print(f"You win ${bet}!")
        return bet
    if p_val < d_val:
        print("Dealer wins.")
        return -bet

    print("Push (tie).")
    return 0


def play_round(bankroll):
    deck = create_deck()
    bet = take_bet(bankroll)

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    print()
    display_hand(dealer_hand, "Dealer", hide_first=True)
    display_hand(player_hand, "Player")
    print()

    # Check blackjack immediately
    if is_blackjack(player_hand) or is_blackjack(dealer_hand):
        display_hand(dealer_hand, "Dealer")
        return bankroll + settle_bet(player_hand, dealer_hand, bet)

    player_hand, new_bet, busted = player_turn(deck, player_hand, bankroll, bet)
    if busted:
        return bankroll - new_bet

    print()
    dealer_hand, dealer_busted = dealer_turn(deck, dealer_hand)

    result = settle_bet(player_hand, dealer_hand, new_bet)
    return bankroll + result


def main():
    bankroll = START_BANKROLL
    print("=== Blackjack Game ===")

    while bankroll >= MIN_BET:
        print(f"\nBankroll: ${bankroll}")
        bankroll = play_round(bankroll)

        again = input("\nPlay another round? (y/n): ").strip().lower()
        if not again.startswith("y"):
            break

    print("\nThanks for playing!")
    print(f"Final bankroll: ${bankroll}")

if __name__ == "__main__":
    main()