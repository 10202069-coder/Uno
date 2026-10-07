import random
import time
from vex import *

# Initialize the VEX EXP Brain
brain = Brain()

def create_uno_deck():
    colors = ['Red', 'Yellow', 'Green', 'Blue']
    values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2']
    deck = []

    for color in colors:
        deck.append(color + "0")
        for val in values:
            deck.append(color + val)
            deck.append(color + val)

    for i in range(4):
        deck.append("Wild")
        deck.append("Wild+4")

    return deck

def shuffle_deck(deck):
    deck_length = len(deck)
    for i in range(deck_length - 1, 0, -1):
        j = random.randint(0, i)
        temp = deck[i]
        deck[i] = deck[j]
        deck[j] = temp

def shorten_card(card):
    c = str(card)
    c = c.replace("Red", "R")
    c = c.replace("Yellow", "Y")
    c = c.replace("Green", "G")
    c = c.replace("Blue", "B")
    c = c.replace("Reverse", "Rev")
    c = c.replace("Skip", "Skp")
    c = c.replace("Wild+4", "W+4")
    c = c.replace("Wild", "Wd")
    return c

def parse_card(card_str):
    if card_str.startswith("Wild+4"):
        return ("Wild", "Wild+4")
    if card_str.startswith("Wild"):
        return ("Wild", "Wild")

    for col in ['Red', 'Yellow', 'Green', 'Blue']:
        if card_str.startswith(col):
            val = card_str[len(col):]
            return (col, val)

    return ("Unknown", "Unknown")

def is_valid_play(card_str, top_card, active_color):
    played_color, played_val = parse_card(card_str)
   
    if played_color == "Wild":
        return True

    top_col, top_val = parse_card(top_card)

    if played_color == active_color:
        return True

    if played_val != "" and played_val == top_val:
        return True

    return False

def select_wild_color_human():
    colors = ['Red', 'Yellow', 'Green', 'Blue']
    idx = 0
    needs_redraw = True

    while True:
        if needs_redraw:
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("PICK NEW COLOR")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(3, 1)
            brain.screen.print(("< " + colors[idx] + " >")[:16])
            brain.screen.set_cursor(4, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(5, 1)
            brain.screen.print("<- -> | CHECK")
            needs_redraw = False

        time.sleep(0.05)

        if brain.buttonLeft.pressing():
            idx = (idx - 1) % len(colors)
            needs_redraw = True
            while brain.buttonLeft.pressing():
                time.sleep(0.05)
        elif brain.buttonRight.pressing():
            idx = (idx + 1) % len(colors)
            needs_redraw = True
            while brain.buttonRight.pressing():
                time.sleep(0.05)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                time.sleep(0.05)
            return colors[idx]

def format_hand_lines(hand):
    lines = []
    current_line = ""
    for card in hand:
        short = shorten_card(card)
        if current_line == "":
            test_line = short
        else:
            test_line = current_line + "," + short
       
        if len(test_line) <= 16:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = short
           
    if current_line != "":
        lines.append(current_line)
       
    return lines

def draw_cards_from_deck(deck, hand, count):
    drawn = []
    for _ in range(count):
        if len(deck) > 0:
            c = deck.pop()
            hand.append(c)
            drawn.append(c)
    return drawn

def handle_skip_screen(player_name, reason="TURN SKIPPED!"):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("================")
    brain.screen.set_cursor(2, 1)
    brain.screen.print((player_name + " SKIPPED")[:16])
    brain.screen.set_cursor(3, 1)
    brain.screen.print(reason[:16])
    brain.screen.set_cursor(4, 1)
    brain.screen.print("================")
    brain.screen.set_cursor(5, 1)
    brain.screen.print(" Passing Turn... ")
    time.sleep(1.8)

def display_human_turn(player_name, hand, deck, top_card, active_color):
    p_name = str(player_name)
   
    print("--- " + p_name + " Hand ---")
    print("Top Card: " + str(top_card) + " (Color: " + active_color + ")")
    for i, card in enumerate(hand):
        valid_mark = " [VALID]" if is_valid_play(card, top_card, active_color) else ""
        print("  " + str(i + 1) + ". " + str(card) + valid_mark)
    print("")

    # 1. Privacy Pass Screen
    pass_msg = "PASS TO " + p_name
    top_msg = "Top:" + shorten_card(top_card) + " (" + active_color[0] + ")"

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("================")
    brain.screen.set_cursor(2, 1)
    brain.screen.print(pass_msg[:16])
    brain.screen.set_cursor(3, 1)
    brain.screen.print(top_msg[:16])
    brain.screen.set_cursor(4, 1)
    brain.screen.print("================")
    brain.screen.set_cursor(5, 1)
    brain.screen.print("[PRESS CHECK]")

    while not brain.buttonCheck.pressing():
        time.sleep(0.05)
    while brain.buttonCheck.pressing():
        time.sleep(0.05)

    # 2. Card Viewing Screen
    brain.screen.clear_screen()
    header_msg = p_name + " (" + str(len(hand)) + ")"
   
    brain.screen.set_cursor(1, 1)
    brain.screen.print(header_msg[:16])
    brain.screen.set_cursor(2, 1)
    brain.screen.print(top_msg[:16])

    card_lines = format_hand_lines(hand)
    for idx in range(2):
        target_row = 3 + idx
        brain.screen.set_cursor(target_row, 1)
        if idx < len(card_lines):
            line = card_lines[idx]
            brain.screen.print(line[:16])
        else:
            brain.screen.print("")

    brain.screen.set_cursor(5, 1)
    brain.screen.print("[PRESS CHECK]")

    while not brain.buttonCheck.pressing():
        time.sleep(0.05)
    while brain.buttonCheck.pressing():
        time.sleep(0.05)

    # 3. Card Picking Screen (With 1-Card Restrictive [SAY UNO!] Option)
    selected_index = 0
    needs_redraw = True
    status_override = ""
    played_card = None
    uno_called = False

    while True:
        uno_opt_index = len(hand)
        draw_opt_index = len(hand) + 1
        total_options = len(hand) + 2

        if selected_index >= total_options:
            selected_index = 0

        if needs_redraw:
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("SELECT ACTION")
           
            brain.screen.set_cursor(2, 1)
            brain.screen.print(top_msg[:16])

            if status_override != "":
                brain.screen.set_cursor(3, 1)
                brain.screen.print(status_override[:16])
                brain.screen.set_cursor(4, 1)
                if status_override == "NEED 1 CARD!":
                    brain.screen.print("Only 1 card left")
                else:
                    brain.screen.print("Match color/num")
            else:
                if selected_index < len(hand):
                    card_str = hand[selected_index]
                    opt_num = str(selected_index + 1) + "/" + str(len(hand))
                    line3 = "< " + shorten_card(card_str) + " (" + opt_num + ") >"
                   
                    if is_valid_play(card_str, top_card, active_color):
                        line4 = "Play: " + card_str
                    else:
                        line4 = "NO MATCH!"

                    brain.screen.set_cursor(3, 1)
                    brain.screen.print(line3[:16])
                    brain.screen.set_cursor(4, 1)
                    brain.screen.print(line4[:16])
                elif selected_index == uno_opt_index:
                    if len(hand) == 1:
                        uno_status = "ACTIVE!" if uno_called else "PRESS CHECK"
                    else:
                        uno_status = "NEED 1 CARD"
                    line3 = "< [SAY UNO!] >"
                    line4 = "UNO: " + uno_status
                    brain.screen.set_cursor(3, 1)
                    brain.screen.print(line3[:16])
                    brain.screen.set_cursor(4, 1)
                    brain.screen.print(line4[:16])
                else: # Draw card option
                    line3 = "< [DRAW CARD] >"
                    line4 = "Draw from deck"
                    brain.screen.set_cursor(3, 1)
                    brain.screen.print(line3[:16])
                    brain.screen.set_cursor(4, 1)
                    brain.screen.print(line4[:16])

            brain.screen.set_cursor(5, 1)
            brain.screen.print("<- -> | CHECK")
            needs_redraw = False

        time.sleep(0.05)
       
        # Navigate left
        if brain.buttonLeft.pressing():
            selected_index = (selected_index - 1) % total_options
            status_override = ""
            needs_redraw = True
            while brain.buttonLeft.pressing():
                time.sleep(0.05)
        # Navigate right
        elif brain.buttonRight.pressing():
            selected_index = (selected_index + 1) % total_options
            status_override = ""
            needs_redraw = True
            while brain.buttonRight.pressing():
                time.sleep(0.05)
        # Confirm selection
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                time.sleep(0.05)
           
            if selected_index < len(hand):
                candidate_card = hand[selected_index]
                if is_valid_play(candidate_card, top_card, active_color):
                    played_card = hand.pop(selected_index)
                    top_card = played_card
                    p_col, _ = parse_card(played_card)

                    if p_col == "Wild":
                        new_color = select_wild_color_human()
                        active_color = new_color
                        print(p_name + " played " + played_card + " and set color to " + active_color)
                    else:
                        active_color = p_col
                        print(p_name + " played: " + str(played_card))

                    # Check for UNO rule when playing final card
                    if len(hand) == 0:
                        if not uno_called:
                            print(p_name + " played their last card WITHOUT saying UNO! (+2 Penalty Cards)")
                            draw_cards_from_deck(deck, hand, 2)
                           
                            brain.screen.clear_screen()
                            brain.screen.set_cursor(1, 1)
                            brain.screen.print("================")
                            brain.screen.set_cursor(2, 1)
                            brain.screen.print(" FORGOT UNO! ")
                            brain.screen.set_cursor(3, 1)
                            brain.screen.print(" +2 CARDS DRAWN ")
                            brain.screen.set_cursor(4, 1)
                            brain.screen.print("================")
                            brain.screen.set_cursor(5, 1)
                            brain.screen.print(" Turn Ending... ")
                            time.sleep(2.0)
                        else:
                            print(p_name + " CALLED UNO AND PLAYED FINAL CARD!")
                    break
                else:
                    status_override = "INVALID MATCH!"
                    needs_redraw = True
            elif selected_index == uno_opt_index:
                # Strictly enforce 1-card restriction for calling UNO
                if len(hand) == 1:
                    uno_called = True
                    print(p_name + " called UNO!")
                    status_override = ""
                    needs_redraw = True
                else:
                    status_override = "NEED 1 CARD!"
                    needs_redraw = True
            else: # Draw Card selected
                played_card = None
                if len(deck) > 0:
                    drawn_card = deck.pop()
                    hand.append(drawn_card)
                    print(p_name + " drew: " + str(drawn_card))
                else:
                    print("Deck is empty!")
                break

    # 4. Conceal Transition Screen
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("================")
    brain.screen.set_cursor(2, 1)
    brain.screen.print(" HAND CONCEALED ")
    brain.screen.set_cursor(3, 1)
    brain.screen.print(" Passing Turn...")
    brain.screen.set_cursor(4, 1)
    brain.screen.print("================")
    brain.screen.set_cursor(5, 1)
    brain.screen.print(" Please Wait... ")
    time.sleep(0.8)

    return top_card, active_color, played_card

def display_robot_turn(player_name, hand, deck, top_card, active_color):
    p_name = str(player_name)
   
    playable_indices = [i for i, card in enumerate(hand) if is_valid_play(card, top_card, active_color)]
    uno_called = False

    if len(playable_indices) > 0:
        # Robot calls UNO only if down to 1 card left
        if len(hand) == 1:
            uno_called = True
            print(p_name + " called UNO!")

        chosen_idx = playable_indices[0]
        played_card = hand.pop(chosen_idx)
        top_card = played_card
        p_col, _ = parse_card(played_card)

        if p_col == "Wild":
            color_counts = {'Red': 0, 'Yellow': 0, 'Green': 0, 'Blue': 0}
            for c in hand:
                col, _ = parse_card(c)
                if col in color_counts:
                    color_counts[col] += 1
            best_color = max(color_counts, key=color_counts.get)
            active_color = best_color
            action_desc = "Played: " + shorten_card(played_card) + " -> " + active_color[:1]
        else:
            active_color = p_col
            action_desc = "Played: " + shorten_card(played_card)

        if len(hand) == 0 and not uno_called:
            print(p_name + " forgot to say UNO! Drawing 2 penalty cards.")
            draw_cards_from_deck(deck, hand, 2)
    else:
        played_card = None
        if len(deck) > 0:
            drawn_card = deck.pop()
            hand.append(drawn_card)
            action_desc = "Drew a card"
        else:
            action_desc = "Passed (Deck Empty)"

    print("--- " + p_name + " Turn (Robot) ---")
    print("Robot action: " + action_desc)
    print("Active Color: " + active_color)
    print("Cards remaining in hand: " + str(len(hand)))
    print("")

    turn_msg = p_name + " TURN"
    hand_size_msg = "Hand size: " + str(len(hand))

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print(turn_msg[:16])
    brain.screen.set_cursor(2, 1)
    brain.screen.print(action_desc[:16])
    brain.screen.set_cursor(3, 1)
    brain.screen.print(("Color: " + active_color)[:16])
    brain.screen.set_cursor(4, 1)
    brain.screen.print(hand_size_msg[:16])
    brain.screen.set_cursor(5, 1)
    brain.screen.print("Auto-Passing...")

    time.sleep(2.0)
    return top_card, active_color, played_card

def setup_and_play():
    deck = create_uno_deck()
    shuffle_deck(deck)

    players = ["Player", "VEX Robot"]
    hands = {}
    for player in players:
        hands[player] = []

    cards_per_player = 7
    for i in range(cards_per_player):
        for player in players:
            if len(deck) > 0:
                hands[player].append(deck.pop())

    if len(deck) > 0:
        top_card = deck.pop()
    else:
        top_card = "Red0"

    initial_color, _ = parse_card(top_card)
    active_color = "Red" if initial_color == "Wild" else initial_color

    print("=== UNO GAME INITIALIZED ===")
    print("Top Card: " + str(top_card) + " | Active Color: " + active_color)
    print("Remaining in Draw Pile: " + str(len(deck)))
    print("")

    current_idx = 0
    pending_draws = 0
    skip_next = False

    while True:
        current_player = players[current_idx]

        # 1. Apply penalty card draws (+2 / +4) to current player
        if pending_draws > 0:
            drawn_cards = draw_cards_from_deck(deck, hands[current_player], pending_draws)
            print(current_player + " drew " + str(len(drawn_cards)) + " penalty card(s)!")
           
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(2, 1)
            brain.screen.print((current_player[:16]))
            brain.screen.set_cursor(3, 1)
            brain.screen.print(("+" + str(pending_draws) + " CARDS DRAWN")[:16])
            brain.screen.set_cursor(4, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(5, 1)
            brain.screen.print(" Please Wait... ")
            time.sleep(1.8)

            pending_draws = 0

        # 2. Apply skip turn condition
        if skip_next:
            print(current_player + "'s turn was SKIPPED!")
            handle_skip_screen(current_player, "TURN SKIPPED!")
            skip_next = False
            current_idx = (current_idx + 1) % len(players)
            continue

        # 3. Process turn
        if current_player == "VEX Robot":
            top_card, active_color, played_card = display_robot_turn(current_player, hands[current_player], deck, top_card, active_color)
        else:
            top_card, active_color, played_card = display_human_turn(current_player, hands[current_player], deck, top_card, active_color)

        # 4. Check for Winner
        if len(hands[current_player]) == 0:
            print("=================================")
            print(current_player + " WINS THE GAME!")
            print("=================================")

            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(2, 1)
            brain.screen.print((current_player[:10] + " WINS!").center(16))
            brain.screen.set_cursor(3, 1)
            brain.screen.print(" GAME OVER! ".center(16))
            brain.screen.set_cursor(4, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(5, 1)
            brain.screen.print(" CONGRATS! ")
            break

        # 5. Trigger special card rules for the next player
        if played_card is not None:
            _, val = parse_card(played_card)
            if val == "Skip":
                skip_next = True
            elif val == "+2":
                pending_draws = 2
            elif val == "Wild+4":
                pending_draws = 4
                skip_next = True

        current_idx = (current_idx + 1) % len(players)

# Execute game
setup_and_play()
