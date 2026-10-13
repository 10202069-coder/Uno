import random
import time
from vex import *

# Initialize VEX EXP Brain and Drive Motors
brain = Brain()
motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)    # Left drive motor
right_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)   # Right drive motor
motor_5 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)      # Auxiliary motor

# Set default motor velocities
motor_1.set_velocity(50, PERCENT)
right_motor.set_velocity(50, PERCENT)
motor_5.set_velocity(50, PERCENT)

# ANSI escape codes for Black text on White background
ANSI_BLACK_BG_WHITE = "\033[30;47m"
ANSI_RESET = "\033[0m"

def print_black(text=""):
    """Output console text in black with white background."""
    print(ANSI_BLACK_BG_WHITE + str(text) + ANSI_RESET)

def fwd(degrees=360):
    """
    Drives the VEX robot straight forward by spinning motor_1 (left drive),
    right_motor (right drive), and motor_5 forward simultaneously.
    """
    motor_1.set_velocity(50, PERCENT)
    right_motor.set_velocity(50, PERCENT)
    motor_5.set_velocity(50, PERCENT)
   
    motor_1.spin_for(FORWARD, degrees, DEGREES, wait=False)
    motor_5.spin_for(FORWARD, degrees, DEGREES, wait=False)
    right_motor.spin_for(FORWARD, degrees, DEGREES, wait=True)
    time.sleep(0.1)  # 0.1s cooldown

def rt(degrees=90):
    """Rotates only the right motor forward by specified degrees."""
    right_motor.set_velocity(40, PERCENT)
    right_motor.spin_for(FORWARD, degrees, DEGREES, wait=True)
    time.sleep(0.1)  # 0.1s cooldown

def lt(degrees=90):
    """Rotates only the left motor (motor_1) forward by specified degrees."""
    motor_1.set_velocity(40, PERCENT)
    motor_1.spin_for(FORWARD, degrees, DEGREES, wait=True)
    time.sleep(0.1)  # 0.1s cooldown

def execute_robot_movement():
    """
    Sequential physical movement sequence:
    1. Forward x2 (fwd, fwd)
    2. Turn Right x2 (rt, rt)
    3. Forward x2 (fwd, fwd)
    4. Turn Right x2 (rt, rt)
    """
    print_black(">>> EXECUTING ROBOT MOVEMENT SEQUENCE <<<")
    fwd(360)
    fwd(360)
    rt(90)
    rt(90)
    fwd(360)
    fwd(360)
    rt(90)
    rt(90)
    """Draws cards from deck and triggers motor movement for each card drawn."""
    drawn = []
    for _ in range(count):
        if len(deck) > 0:
            c = deck.pop()
            hand.append(c)
            drawn.append(c)
            execute_robot_movement()
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

def display_human_turn(player_name, hand, robot_hand, deck, top_card, active_color):
    p_name = str(player_name)
   
    print_black("---------------------------------")
    print_black("=== " + p_name.upper() + "'S TURN ===")
    print_black("Top Card: " + str(top_card) + " (Active Color: " + active_color + ")")
    print_black("Shared Draw Deck Remaining: " + str(len(deck)) + " cards")
    print_black("Player Hand (" + str(len(hand)) + " cards):")
    for i, card in enumerate(hand):
        valid_mark = " [PLAYABLE]" if is_valid_play(card, top_card, active_color) else ""
        print_black("  " + str(i + 1) + ". " + str(card) + valid_mark)
    print_black("VEX Robot Hand (" + str(len(robot_hand)) + " cards): " + str(robot_hand))
    print_black("---------------------------------")
    selected_index = 0
    needs_redraw = True
    status_override = ""
    played_card = None
    uno_called = False

    while True:
        has_uno_opt = (len(hand) == 1)
        if has_uno_opt:
            uno_opt_index = len(hand)
            draw_opt_index = len(hand) + 1
            total_options = len(hand) + 2
        else:
            uno_opt_index = -1
            draw_opt_index = len(hand)
            total_options = len(hand) + 1

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
                    uno_status = "ACTIVE!" if uno_called else "PRESS CHECK"
                    line3 = "< [SAY UNO!] >"
                    line4 = "UNO: " + uno_status
                    brain.screen.set_cursor(3, 1)
                    brain.screen.print(line3[:16])
                    brain.screen.set_cursor(4, 1)
                    brain.screen.print(line4[:16])
                else:
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

        if brain.buttonLeft.pressing():
            selected_index = (selected_index - 1) % total_options
            status_override = ""
            needs_redraw = True
            while brain.buttonLeft.pressing():
                time.sleep(0.05)
        elif brain.buttonRight.pressing():
            selected_index = (selected_index + 1) % total_options
            status_override = ""
            needs_redraw = True
            while brain.buttonRight.pressing():
                time.sleep(0.05)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                time.sleep(0.05)
           
            if selected_index < len(hand):
                candidate_card = hand[selected_index]
                if is_valid_play(candidate_card, top_card, active_color):
                    played_card = hand.pop(selected_index)
                    top_card = played_card
                    p_col, _ = parse_card(played_card)

                    print_black(">>> " + p_name + " PLAYED CARD: " + str(played_card) + " <<<")

                    if p_col == "Wild":
                        new_color = select_wild_color_human()
                        active_color = new_color
                        print_black(">>> " + p_name + " CHANGED ACTIVE COLOR TO: " + active_color + " <<<")
                    else:
                        active_color = p_col

                    execute_robot_movement()

                    if len(hand) == 0:
                        if not uno_called:
                            print_black("!!! " + p_name + " played last card WITHOUT saying UNO! (+2 Penalty Cards) !!!")
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
                            print_black("*** " + p_name + " CALLED UNO AND PLAYED FINAL CARD! ***")
                    break
                else:
                    status_override = "INVALID MATCH!"
                    needs_redraw = True
            elif selected_index == uno_opt_index:
                uno_called = True
                print_black(">>> " + p_name + " CALLED UNO! <<<")
                status_override = ""
                needs_redraw = True
            else:
                played_card = None
                if len(deck) > 0:
                    drawn_cards = draw_cards_from_deck(deck, hand, 1)
                    print_black(">>> " + p_name + " DREW CARD FROM SHARED DECK: " + str(drawn_cards[0]) + " <<<")
                else:
                    print_black("!!! Shared Draw Deck is empty! !!!")
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

def display_robot_turn(player_name, hand, player_hand, deck, top_card, active_color):
    p_name = str(player_name)
   
    playable_indices = [i for i, card in enumerate(hand) if is_valid_play(card, top_card, active_color)]
    uno_called = False

    print_black("---------------------------------")
    print_black("=== " + p_name.upper() + "'S TURN (ROBOT) ===")
    print_black("Top Card: " + str(top_card) + " (Active Color: " + active_color + ")")
    print_black("Shared Draw Deck Remaining: " + str(len(deck)) + " cards")
    print_black("Robot Hand (" + str(len(hand)) + " cards): " + str(hand))
    print_black("Player Hand (" + str(len(player_hand)) + " cards): " + str(player_hand))

    if len(playable_indices) > 0:
        if len(hand) == 1:
            uno_called = True
            print_black(">>> " + p_name + " CALLED UNO! <<<")

        chosen_idx = playable_indices[0]
        played_card = hand.pop(chosen_idx)
        top_card = played_card
        p_col, _ = parse_card(played_card)

        print_black(">>> ROBOT PLAYED CARD: " + str(played_card) + " <<<")

        if p_col == "Wild":
            color_counts = {'Red': 0, 'Yellow': 0, 'Green': 0, 'Blue': 0}
            for c in hand:
                col, _ = parse_card(c)
                if col in color_counts:
                    color_counts[col] += 1
            best_color = max(color_counts, key=color_counts.get)
            active_color = best_color
            print_black(">>> ROBOT CHANGED ACTIVE COLOR TO: " + active_color + " <<<")
            action_desc = "Played: " + shorten_card(played_card) + " -> " + active_color[:1]
        else:
            active_color = p_col
            action_desc = "Played: " + shorten_card(played_card)

        execute_robot_movement()

        if len(hand) == 0 and not uno_called:
            print_black("!!! " + p_name + " forgot to say UNO! Drawing 2 penalty cards. !!!")
            draw_cards_from_deck(deck, hand, 2)
    else:
        played_card = None
        if len(deck) > 0:
            drawn_cards = draw_cards_from_deck(deck, hand, 1)
            print_black(">>> ROBOT DREW CARD FROM SHARED DECK: " + str(drawn_cards[0]) + " <<<")
            action_desc = "Drew a card"
        else:
            print_black("!!! Shared Draw Deck is empty! !!!")
            action_desc = "Passed (Deck Empty)"

    print_black("Cards remaining in Robot hand: " + str(len(hand)))
    print_black("---------------------------------")

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
    shared_deck = create_uno_deck()
    shuffle_deck(shared_deck)

    players = ["Player", "VEX Robot"]
    hands = {"Player": [], "VEX Robot": []}

    cards_per_player = 7
    for i in range(cards_per_player):
        for player in players:
            if len(shared_deck) > 0:
                hands[player].append(shared_deck.pop())

    if len(shared_deck) > 0:
        top_card = shared_deck.pop()
    else:
        top_card = "Red0"

    initial_color, _ = parse_card(top_card)
    active_color = "Red" if initial_color == "Wild" else initial_color

    print_black("=========================================")
    print_black("=== UNO GAME INITIALIZED (FULL ROBOT FORWARD DRIVE) ===")
    print_black("Top Starting Card: " + str(top_card) + " | Active Color: " + active_color)
    print_black("Shared Draw Deck Count: " + str(len(shared_deck)) + " cards")
    print_black("Player Hand (" + str(len(hands["Player"])) + " cards): " + str(hands["Player"]))
    print_black("Robot Hand (" + str(len(hands["VEX Robot"])) + " cards): " + str(hands["VEX Robot"]))
    print_black("=========================================")
    print_black("")

    current_idx = 0
    pending_draws = 0
    skip_next = False

    while True:
        current_player = players[current_idx]

        if pending_draws > 0:
            drawn_cards = draw_cards_from_deck(shared_deck, hands[current_player], pending_draws)
            print_black(">>> " + current_player + " DREW " + str(len(drawn_cards)) + " PENALTY CARD(S): " + str(drawn_cards) + " <<<")
           
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

        if skip_next:
            print_black(">>> " + current_player + "'S TURN WAS SKIPPED! <<<")
            handle_skip_screen(current_player, "TURN SKIPPED!")
            skip_next = False
            current_idx = (current_idx + 1) % len(players)
            continue

        if current_player == "VEX Robot":
            top_card, active_color, played_card = display_robot_turn(
                current_player, hands["VEX Robot"], hands["Player"], shared_deck, top_card, active_color
            )
        else:
            top_card, active_color, played_card = display_human_turn(
                current_player, hands["Player"], hands["VEX Robot"], shared_deck, top_card, active_color
            )

        if len(hands[current_player]) == 0:
            print_black("=================================")
            print_black("=== " + current_player.upper() + " WINS THE GAME! ===")
            print_black("=================================")

            win_msg = current_player[:10] + " WINS!"
            pad1 = (16 - len(win_msg)) // 2
            win_line = (" " * max(0, pad1)) + win_msg

            over_msg = "GAME OVER!"
            pad2 = (16 - len(over_msg)) // 2
            over_line = (" " * max(0, pad2)) + over_msg

            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(2, 1)
            brain.screen.print(win_line[:16])
            brain.screen.set_cursor(3, 1)
            brain.screen.print(over_line[:16])
            brain.screen.set_cursor(4, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(5, 1)
            brain.screen.print("  CONGRATS!  ")
            break

        if played_card is not None:
            _, val = parse_card(played_card)
            if val == "Skip" or val == "Reverse":
                skip_next = True
            elif val == "+2":
                pending_draws = 2
                skip_next = True
            elif val == "Wild+4":
                pending_draws = 4
                skip_next = True

        current_idx = (current_idx + 1) % len(players)

setup_and_play()
