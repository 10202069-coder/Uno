import random
import time
from vex import *

# Initialize VEX EXP Brain and Drive Motors
brain = Brain()
motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)    # Left drive motor (Port 1)
motor_5 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)     # Right drive motor (Port 5)

# Set default motor velocities (30% velocity for softer movement)
motor_1.set_velocity(30, PERCENT)
motor_5.set_velocity(30, PERCENT)

# ANSI escape codes for Black text on White background
ANSI_BLACK_BG_WHITE = "\033[30;47m"
ANSI_RESET = "\033[0m"

def print_black(text=""):
    """Output console text in black with white background."""
    print(ANSI_BLACK_BG_WHITE + str(text) + ANSI_RESET)

def fwd(duration=0.4):
    """
    Drives forward using motor_1 (Port 1) and motor_5 (Port 5) simultaneously.
    Runs at 30% velocity for a soft, smooth drive motion.
    """
    motor_1.set_velocity(30, PERCENT)
    motor_5.set_velocity(30, PERCENT)
    
    motor_1.spin(FORWARD)
    motor_5.spin(FORWARD)
    
    time.sleep(duration)
    
    motor_1.stop(HOLD)
    motor_5.stop(HOLD)
    time.sleep(0.1)  # 0.1s cooldown pause

def rt(degrees=235):
    """
    Spins the robot right in place by driving motor_1 forward 
    and motor_5 in reverse simultaneously by 235 degrees.
    """
    motor_1.set_velocity(30, PERCENT)
    motor_5.set_velocity(30, PERCENT)
    motor_1.spin_for(FORWARD, degrees, DEGREES, wait=False)
    motor_5.spin_for(REVERSE, degrees, DEGREES, wait=True)
    time.sleep(0.1)  # 0.1s cooldown pause

def lt(degrees=235):
    """
    Spins the robot left in place by driving motor_1 in reverse 
    and motor_5 forward simultaneously by 235 degrees.
    """
    motor_1.set_velocity(30, PERCENT)
    motor_5.set_velocity(30, PERCENT)
    motor_1.spin_for(REVERSE, degrees, DEGREES, wait=False)
    motor_5.spin_for(FORWARD, degrees, DEGREES, wait=True)
    time.sleep(0.1)  # 0.1s cooldown pause

def execute_robot_movement():
    """
    Sequential physical movement sequence:
    Forward x2 -> Clear Screen -> Turn Right 235° x2 -> Forward x2 -> Turn Right 235° x2
    """
    print_black(">>> EXECUTING ROBOT MOVEMENT SEQUENCE <<<")
    fwd(0.4)
    fwd(0.4)
    brain.screen.clear_screen()
    rt(235)
    rt(235)
    fwd(0.4)
    fwd(0.4)
    rt(235)
    rt(235)

def draw_card_full_screen(card_str, color_code):
    """Renders full screen graphical card graphic on VEX Brain screen."""
    brain.screen.clear_screen()
    if color_code == 'R':
        brain.screen.set_fill_color(Color.RED)
    elif color_code == 'G':
        brain.screen.set_fill_color(Color.GREEN)
    elif color_code == 'B':
        brain.screen.set_fill_color(Color.BLUE)
    elif color_code == 'Y':
        brain.screen.set_fill_color(Color.YELLOW)
    else:
        brain.screen.set_fill_color(Color.BLACK)

    brain.screen.set_pen_color(Color.WHITE)
    for i in range(5):
        brain.screen.draw_rectangle(0+i, 0+i, 159-(i*2), 107-(i*2))
   
    card = card_str[1:] if len(card_str) > 1 else ""
    if card == "0":
        for i in range(15):
            brain.screen.draw_rectangle(20+i, 20+i, 119-(i*2), 67-(i*2))
    elif card == "8":
        for i in range(15):
            brain.screen.draw_rectangle(20+i, 20+i, 119-(i*2), 67-(i*2))
        for i in range(15):
            brain.screen.draw_line(72+i, 20, 72+i, 85)
    elif card == "1":
        for i in range(15):
            brain.screen.draw_line(20, 47+i, 139, 47+i)
    elif card == "3":
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 139, 20+i)
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
    elif card == "2":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 73+i, 139, 73+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "5":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "6":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
            brain.screen.draw_line(72, 73+i, 139, 73+i)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "9":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "4" and "D" not in card_str:
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
    elif card == "7":
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 139, 20+i)
            brain.screen.draw_line(20+i, 20, 20+i, 87)
    elif card == "Rv":
        for i in range(15):
            brain.screen.draw_line(62+i, 30, 62+i, 87)
            brain.screen.draw_line(69, 20, 52+i, 40)
            brain.screen.draw_line(69, 20, 82-i, 40)
            brain.screen.draw_line(82+i, 20, 82+i, 77)
            brain.screen.draw_line(89, 87, 74+i, 67)
            brain.screen.draw_line(89, 87, 104-i, 67)
    elif card == "S":
        for i in range(15):
            brain.screen.draw_rectangle(40+i, 20+i, 82-(i*2), 67-(i*2))
        for i in range(15):
            brain.screen.draw_line(52+i, 20, 92+i, 80)
    elif card == "D2":
        brain.screen.set_fill_color(Color.WHITE)
        for i in range(40):
            brain.screen.draw_circle(int(60+(i/1)), int(42+(i/2)), 30)
        if color_code == 'R':
            brain.screen.set_fill_color(Color.RED)
        elif color_code == 'G':
            brain.screen.set_fill_color(Color.GREEN)
        elif color_code == 'B':
            brain.screen.set_fill_color(Color.BLUE)
        elif color_code == 'Y':
            brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(47, 32, 40, 25)
        brain.screen.draw_rectangle(73, 52, 40, 25)
        for i in range(5):
            brain.screen.draw_line(18+i, 85, 18+i, 95)
            brain.screen.draw_line(14, 88+i, 26, 88+i)
            brain.screen.draw_line(10+i, 66, 10+i, 79)
            brain.screen.draw_line(10, 66+i, 20, 66+i)
            brain.screen.draw_line(18+i, 66, 18+i, 79)
            brain.screen.draw_line(20, 75+i, 30, 75+i)
            brain.screen.draw_line(26+i, 66, 26+i, 79)

            brain.screen.draw_line(159-18-i, 107-85, 159-18-i, 107-95)
            brain.screen.draw_line(159-14, 107-88-i, 159-26, 107-88-i)
            brain.screen.draw_line(159-10-i, 107-66, 159-10-i, 107-79)
            brain.screen.draw_line(159-10, 107-66-i, 159-20, 107-66-i)
            brain.screen.draw_line(159-18-i, 107-66, 159-18-i, 107-79)
            brain.screen.draw_line(159-20, 107-75-i, 159-30, 107-75-i)
            brain.screen.draw_line(159-26-i, 107-66, 159-26-i, 107-79)
    elif card_str == "W":
        brain.screen.set_fill_color(Color.BLUE)
        brain.screen.draw_rectangle(50, 20, 30, 32)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(50, 52, 30, 32)
        brain.screen.set_fill_color(Color.GREEN)
        brain.screen.draw_rectangle(80, 20, 30, 32)
        brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(80, 52, 30, 32)
        brain.screen.set_fill_color(Color.TRANSPARENT)
        brain.screen.set_pen_width(3)
        for i in range(15):
            brain.screen.draw_circle(80, 52, int(30-(i/5)))
        brain.screen.set_pen_color(Color.BLACK)
        for i in range(65):
            brain.screen.draw_circle(80, 52, int(31+(i/5)))
        brain.screen.set_pen_width(1)
    elif card_str == "D4":
        brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(78, 42, 40, 25)
        brain.screen.set_fill_color(Color.GREEN)
        brain.screen.draw_rectangle(60, 28, 40, 25)
        brain.screen.set_fill_color(Color.BLUE)
        brain.screen.draw_rectangle(42, 42, 40, 25)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(60, 56, 40, 25)
        for i in range(5):
            brain.screen.draw_line(18+i, 85, 18+i, 95)
            brain.screen.draw_line(14, 88+i, 26, 88+i)
            brain.screen.draw_line(10, 75+i, 20, 75+i)
            brain.screen.draw_line(16+i, 75, 16+i, 66)
            brain.screen.draw_line(10, 66+i, 30, 66+i)

            brain.screen.draw_line(159-18-i, 107-85, 159-18-i, 107-95)
            brain.screen.draw_line(159-14, 107-88-i, 159-26, 107-88-i)
            brain.screen.draw_line(159-10, 107-75-i, 159-20, 107-75-i)
            brain.screen.draw_line(159-16-i, 107-75, 159-16-i, 107-66)
            brain.screen.draw_line(159-10, 107-66-i, 159-30, 107-66-i)
    else:
        brain.screen.set_fill_color(Color.RED)
        brain.screen.set_pen_color(Color.RED)
        for i in range(40):
            brain.screen.draw_circle(int(60+(i/1)), int(42+(i/2)), 30)
        brain.screen.set_pen_color(Color.YELLOW)
        for i in range(5):
            brain.screen.draw_line(75, int(50+i-5), 85, int(50+i-5))
            brain.screen.draw_line(75, int(50+i+5), 85, int(50+i+5))
            brain.screen.draw_line(75, int(50+i+5), 85, int(50+i-5))

            brain.screen.draw_line(75, int(50+i-15), 85, int(50+i-15))
            brain.screen.draw_line(int(75+(i/2)), 50-15, int(75+(i/2)), 50-25)
            brain.screen.draw_line(int(83+(i/2)), 50-15, int(83+(i/2)), 50-25)
            brain.screen.draw_line(75, int(50+i-25), 85, int(50+i-25))

            brain.screen.draw_line(75, int(50+i+15), 85, int(50+i+15))
            brain.screen.draw_line(int(83+(i/2)), 50+15, int(83+(i/2)), 50+25)
            brain.screen.draw_line(75, int(50+i+25), 85, int(50+i+25))
            
    brain.screen.set_fill_color(Color.TRANSPARENT)

def trigger_card_display(played_card, active_color):
    """Parses a played or drawn card string and renders its full-screen graphic."""
    if not played_card:
        return
    p_col, p_val = parse_card(played_card)
    
    if p_col == "Wild":
        color_code = active_color[0].upper() if active_color else 'W'
        if p_val == "Wild+4":
            c_str = "D4"
        else:
            c_str = "W"
    else:
        color_code = p_col[0].upper()
        val_map = {
            "Skip": "S",
            "Reverse": "Rv",
            "+2": "D2"
        }
        mapped_val = val_map.get(p_val, p_val)
        c_str = color_code + mapped_val

    draw_card_full_screen(c_str, color_code)

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

def draw_cards_from_deck(deck, hand, count, active_color="Red"):
    """Draws cards from shared deck, renders the card graphic on screen, and executes movement sequence."""
    drawn = []
    for _ in range(count):
        if len(deck) > 0:
            c = deck.pop()
            hand.append(c)
            drawn.append(c)
            trigger_card_display(c, active_color)
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

    # 3. Card Picking Screen
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

                    trigger_card_display(played_card, active_color)
                    execute_robot_movement()

                    if len(hand) == 0:
                        if not uno_called:
                            print_black("!!! " + p_name + " played last card WITHOUT saying UNO! (+2 Penalty Cards) !!!")
                            draw_cards_from_deck(deck, hand, 2, active_color)
                            
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
                if not uno_called:
                    brain.play_sound(SoundType.BELL)  # Native VEX SoundType for single chime tone
                    uno_called = True
                print_black(">>> " + p_name + " CALLED UNO! <<<")
                status_override = ""
                needs_redraw = True
            else:
                played_card = None
                if len(deck) > 0:
                    drawn_cards = draw_cards_from_deck(deck, hand, 1, active_color)
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
            brain.play_sound(SoundType.BELL)  # Native VEX SoundType for single chime tone
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

        trigger_card_display(played_card, active_color)
        execute_robot_movement()

        if len(hand) == 0 and not uno_called:
            print_black("!!! " + p_name + " forgot to say UNO! Drawing 2 penalty cards. !!!")
            draw_cards_from_deck(deck, hand, 2, active_color)
    else:
        played_card = None
        if len(deck) > 0:
            drawn_cards = draw_cards_from_deck(deck, hand, 1, active_color)
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
    print_black("=== UNO GAME INITIALIZED (FIXED SoundType.BELL) ===")
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
            drawn_cards = draw_cards_from_deck(shared_deck, hands[current_player], pending_draws, active_color)
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

            # Play victory sound sequence using native VEX SoundType
            brain.play_sound(SoundType.TADA)

            # Display big WINNER! text on brain screen
            brain.screen.clear_screen()
            brain.screen.set_font(FontType.PROP40)
            brain.screen.set_pen_color(Color.YELLOW)
            brain.screen.print_at("WINNER!", 12, 60)

            # Slowly spin around in place for ~2 seconds
            motor_1.set_velocity(15, PERCENT)
            motor_5.set_velocity(15, PERCENT)
            motor_1.spin(FORWARD)
            motor_5.spin(REVERSE)
            time.sleep(2.0)

            motor_1.stop(HOLD)
            motor_5.stop(HOLD)
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