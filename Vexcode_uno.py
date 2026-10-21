import random
import time
from vex import *

# Initialize VEX EXP Brain and Drive Motors
brain = Brain()
motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)    # Left drive motor (Port 1)
motor_5 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)     # Right drive motor (Port 5)

# Set default motor velocities (15% velocity for slower, smoother movement)
motor_1.set_velocity(15, PERCENT)
motor_5.set_velocity(15, PERCENT)

# ANSI escape codes for Black text on White background
ANSI_BLACK_BG_WHITE = "\033[30;47m"
ANSI_RESET = "\033[0m"

def print_black(text=""):
    """Output console text in black with white background."""
    print(ANSI_BLACK_BG_WHITE + str(text) + ANSI_RESET)

def fwd(duration=1.2):
    """
    Drives forward using motor_1 (Port 1) and motor_5 (Port 5) simultaneously.
    Runs at 15% velocity for 1.2 seconds for longer forward travel distance.
    """
    motor_1.set_velocity(15, PERCENT)
    motor_5.set_velocity(15, PERCENT)
   
    motor_1.spin(FORWARD)
    motor_5.spin(FORWARD)
   
    time.sleep(duration)
   
    motor_1.stop(HOLD)
    motor_5.stop(HOLD)
    time.sleep(0.1)  # 0.1s cooldown pause

def rt(degrees=235):
    """
    Spins the robot right in place by driving motor_1 forward
    and motor_5 in reverse simultaneously by 235 degrees at 15% velocity.
    """
    motor_1.set_velocity(15, PERCENT)
    motor_5.set_velocity(15, PERCENT)
    motor_1.spin_for(FORWARD, degrees, DEGREES, wait=False)
    motor_5.spin_for(REVERSE, degrees, DEGREES, wait=True)
    time.sleep(0.1)  # 0.1s cooldown pause

def lt(degrees=235):
    """
    Spins the robot left in place by driving motor_1 in reverse
    and motor_5 forward simultaneously by 235 degrees at 15% velocity.
    """
    motor_1.set_velocity(15, PERCENT)
    motor_5.set_velocity(15, PERCENT)
    motor_1.spin_for(REVERSE, degrees, DEGREES, wait=False)
    motor_5.spin_for(FORWARD, degrees, DEGREES, wait=True)
    time.sleep(0.1)  # 0.1s cooldown pause

def execute_robot_movement():
    """
    Sequential physical movement sequence for card plays:
    Forward x2 -> Clear Screen (card disappears) -> Turn Right 235° x2 -> Forward x2 -> Turn Right 235° x2
    """
    print_black(">>> EXECUTING ROBOT MOVEMENT SEQUENCE <<<")
    fwd(1.2)
    fwd(1.2)
    brain.screen.clear_screen()  # Card graphic disappears after moving forward twice
    rt(235)
    rt(235)
    fwd(1.2)
    fwd(1.2)
    rt(235)
    rt(235)

def trigger_victory_sequence(winner_name="Player"):
    """Triggers victory sound, animated confetti graphics, congratulations screen, and a 2-second robot spin."""
    print_black("=================================")
    print_black("=== " + str(winner_name).upper() + " WINS THE GAME! ===")
    print_black("=================================")

    # Play victory sound
    brain.play_sound(SoundType.TADA)

    # Start 2-second celebration spin
    motor_1.set_velocity(15, PERCENT)
    motor_5.set_velocity(15, PERCENT)
    motor_1.spin(FORWARD)
    motor_5.spin(REVERSE)

    # Animated Confetti & Victory Screen (~2 seconds duration)
    confetti_colors = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.WHITE, Color.PURPLE, Color.ORANGE]

    start_time = time.time()
    while (time.time() - start_time) < 2.0:
        brain.screen.clear_screen()
       
        # Render randomized confetti particles across screen
        for _ in range(40):
            cx = random.randint(2, 155)
            cy = random.randint(2, 103)
            ccol = random.choice(confetti_colors)
            brain.screen.set_fill_color(ccol)
            brain.screen.set_pen_color(ccol)
            c_size = random.randint(2, 5)
            brain.screen.draw_rectangle(cx, cy, c_size, c_size)

        # Overlay Banner Box
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.draw_rectangle(12, 15, 136, 78)

        # Draw Banner Text
        brain.screen.set_pen_color(Color.YELLOW)
        brain.screen.set_cursor(2, 3)
        brain.screen.print("CONGRATS!")

        # Render Player win string in GREEN
        brain.screen.set_pen_color(Color.GREEN)
        raw_win_str = str(winner_name) + " WINS!"
        win_str = raw_win_str[:14] if len(raw_win_str) > 14 else raw_win_str

        brain.screen.set_cursor(3, 2)
        brain.screen.print(win_str)

        brain.screen.set_pen_color(Color.CYAN)
        brain.screen.set_cursor(4, 2)
        brain.screen.print("=== WINNER! ===")

        time.sleep(0.12)

    # Stop drive motors after 2-second spin completes
    motor_1.stop(HOLD)
    motor_5.stop(HOLD)

    # Reset screen defaults
    brain.screen.set_fill_color(Color.TRANSPARENT)
    brain.screen.set_pen_color(Color.WHITE)

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
            brain.screen.draw_line(159-10, 107-66, 159-10, 107-79)
            brain.screen.draw_line(159-10, 107-75-i, 159-20, 107-75-i)
            brain.screen.draw_line(159-16-i, 107-75, 159-16-i, 107-66)
            brain.screen.draw_line(159-10, 107-66-i, 159-30, 107-66-i)
    else:
        # Standard UNO Card Back Graphic
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
           
    # Reset both fill color and pen color back to defaults
    brain.screen.set_fill_color(Color.TRANSPARENT)
    brain.screen.set_pen_color(Color.WHITE)

def trigger_card_display(played_card, active_color):
    """Parses a played card string and renders its full-screen graphic."""
    if not played_card:
        return
    p_col, p_val = parse_card(played_card)
   
    if p_col == "Wild":
        color_code = active_color[0].upper() if (active_color and active_color in ['Red', 'Yellow', 'Green', 'Blue']) else 'R'
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
    if not top_card:
        return True

    played_color, played_val = parse_card(card_str)
   
    if played_color == "Wild":
        return True

    top_col, top_val = parse_card(top_card)

    if played_color == active_color:
        return True

    if played_val != "" and played_val == top_val:
        return True

    return False

def select_incoming_attack():
    """Renders UI menu to check for incoming attack options: DRAW NONE, DRAW 2, DRAW 4."""
    options = ["DRAW NONE", "DRAW 2", "DRAW 4"]
    idx = 0
    needs_redraw = True

    while True:
        if needs_redraw:
            brain.screen.clear_screen()
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_cursor(1, 1)
            brain.screen.print("INCOMING ATTACK?")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(3, 1)
            brain.screen.print(("< " + options[idx] + " >")[:16])
            brain.screen.set_cursor(4, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(5, 1)
            brain.screen.print("<- -> | CHECK")
            needs_redraw = False

        time.sleep(0.05)

        if brain.buttonLeft.pressing():
            idx = (idx - 1) % len(options)
            needs_redraw = True
            while brain.buttonLeft.pressing():
                time.sleep(0.05)
        elif brain.buttonRight.pressing():
            idx = (idx + 1) % len(options)
            needs_redraw = True
            while brain.buttonRight.pressing():
                time.sleep(0.05)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                time.sleep(0.05)
            return options[idx]

def declare_color_prompt():
    """Displays DECLARE A COLOR prompt and requires pressing CHECK to continue."""
    brain.screen.clear_screen()
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.set_cursor(1, 1)
    brain.screen.print("DECLARE A COLOR")
    brain.screen.set_cursor(2, 1)
    brain.screen.print("================")
    brain.screen.set_cursor(3, 1)
    brain.screen.print("ok")
    brain.screen.set_cursor(4, 1)
    brain.screen.print("")
    brain.screen.set_cursor(5, 1)
    brain.screen.print("[PRESS CHECK]")

    while not brain.buttonCheck.pressing():
        time.sleep(0.05)
    while brain.buttonCheck.pressing():
        time.sleep(0.05)

def select_top_card_manual():
    """Renders menus to select the top card color and then the card number/value."""
    colors = ['Red', 'Yellow', 'Green', 'Blue']
    values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2']
   
    # 1. Select Color
    c_idx = 0
    needs_redraw = True
    while True:
        if needs_redraw:
            brain.screen.clear_screen()
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_cursor(1, 1)
            brain.screen.print("TOP CARD COLOR")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(3, 1)
            brain.screen.print(("< " + colors[c_idx] + " >")[:16])
            brain.screen.set_cursor(4, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(5, 1)
            brain.screen.print("<- -> | CHECK")
            needs_redraw = False

        time.sleep(0.05)

        if brain.buttonLeft.pressing():
            c_idx = (c_idx - 1) % len(colors)
            needs_redraw = True
            while brain.buttonLeft.pressing():
                time.sleep(0.05)
        elif brain.buttonRight.pressing():
            c_idx = (c_idx + 1) % len(colors)
            needs_redraw = True
            while brain.buttonRight.pressing():
                time.sleep(0.05)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                time.sleep(0.05)
            chosen_color = colors[c_idx]
            break

    # 2. Select Value / Number
    v_idx = 0
    needs_redraw = True
    while True:
        if needs_redraw:
            brain.screen.clear_screen()
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_cursor(1, 1)
            brain.screen.print("TOP CARD VALUE")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(3, 1)
            brain.screen.print(("< " + values[v_idx] + " >")[:16])
            brain.screen.set_cursor(4, 1)
            brain.screen.print("================")
            brain.screen.set_cursor(5, 1)
            brain.screen.print("<- -> | CHECK")
            needs_redraw = False

        time.sleep(0.05)

        if brain.buttonLeft.pressing():
            v_idx = (v_idx - 1) % len(values)
            needs_redraw = True
            while brain.buttonLeft.pressing():
                time.sleep(0.05)
        elif brain.buttonRight.pressing():
            v_idx = (v_idx + 1) % len(values)
            needs_redraw = True
            while brain.buttonRight.pressing():
                time.sleep(0.05)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                time.sleep(0.05)
            chosen_val = values[v_idx]
            break

    selected_top = chosen_color + chosen_val
    return selected_top, chosen_color

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
    """
    Moves forward twice first, flashes each drawn card on screen,
    clears the screen, and completes the remaining movement cycle.
    """
    print_black(">>> EXECUTING ROBOT MOVEMENT & DRAW SEQUENCE <<<")
   
    # 1. Robot moves forward twice
    fwd(1.2)
    fwd(1.2)

    # 2. Flash cards on screen during drawing
    drawn = []
    for _ in range(count):
        if len(deck) > 0:
            c = deck.pop()
            hand.append(c)
            drawn.append(c)
           
            draw_card_full_screen("BACK", "BLACK")
            time.sleep(0.3)
            brain.screen.clear_screen()
            time.sleep(0.1)

    # 3. Disappear (screen cleared) until movement cycle finishes
    brain.screen.clear_screen()

    # 4. Finish remaining movement cycle
    rt(235)
    rt(235)
    fwd(1.2)
    fwd(1.2)
    rt(235)
    rt(235)

    return drawn

def handle_skip_screen(player_name, reason="TURN SKIPPED!"):
    brain.screen.clear_screen()
    brain.screen.set_pen_color(Color.WHITE)
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
   
    print_black("---------------------------------")
    print_black("=== " + p_name.upper() + "'S TURN ===")
    print_black("Top Card: " + str(top_card) + " (Active Color: " + active_color + ")")
    print_black("Shared Draw Deck Remaining: " + str(len(deck)) + " cards")
    print_black("Current Hand (" + str(len(hand)) + " cards):")
    for i, card in enumerate(hand):
        valid_mark = " [PLAYABLE]" if is_valid_play(card, top_card, active_color) else ""
        print_black("  " + str(i + 1) + ". " + str(card) + valid_mark)
    print_black("---------------------------------")

    # 1. Card Viewing Screen (Top card text omitted)
    brain.screen.clear_screen()
    brain.screen.set_pen_color(Color.WHITE)
   
    brain.screen.set_cursor(1, 1)
    brain.screen.print("")
    brain.screen.set_cursor(2, 1)
    brain.screen.print("")

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

    # 2. Incoming Attack Selection Menu
    attack_choice = select_incoming_attack()
    if attack_choice == "DRAW 2":
        print_black(">>> " + p_name + " ACCEPTED DRAW 2 ATTACK <<<")
        draw_cards_from_deck(deck, hand, 2, active_color)
        handle_skip_screen(p_name, "+2 ATTACK SKIPPED")
        return top_card, active_color, None
    elif attack_choice == "DRAW 4":
        print_black(">>> " + p_name + " ACCEPTED DRAW 4 ATTACK <<<")
        draw_cards_from_deck(deck, hand, 4, active_color)
        handle_skip_screen(p_name, "+4 ATTACK SKIPPED")
        return top_card, active_color, None

    # 3. Pick Top Card Menu (Color then Number)
    top_card, active_color = select_top_card_manual()
    top_msg = "Top:" + shorten_card(top_card) + " (" + active_color[0] + ")"

    # 4. Card Picking Screen (Only playable cards in hand are shown/selectable)
    selected_index = 0
    needs_redraw = True
    status_override = ""
    played_card = None

    while True:
        # Filter hand to list only valid playable cards
        playable_indices = [i for i, card in enumerate(hand) if is_valid_play(card, top_card, active_color)]
        num_playable = len(playable_indices)

        draw_opt_index = num_playable
        total_options = num_playable + 1

        if selected_index >= total_options:
            selected_index = 0

        if needs_redraw:
            if status_override != "":
                brain.screen.clear_screen()
                brain.screen.set_pen_color(Color.WHITE)
                brain.screen.set_cursor(2, 1)
                brain.screen.print(" INVALID MATCH! ")
                brain.screen.set_cursor(3, 1)
                brain.screen.print(" Match color/num")
                time.sleep(1.0)
                status_override = ""
                needs_redraw = True
                continue
            else:
                if selected_index < num_playable:
                    orig_idx = playable_indices[selected_index]
                    card_str = hand[orig_idx]
                    trigger_card_display(card_str, active_color)
                    brain.screen.set_pen_color(Color.WHITE)
                    brain.screen.set_cursor(1, 1)
                    brain.screen.print(top_msg[:16])
                else:
                    draw_card_full_screen("BACK", "BLACK")
                    brain.screen.set_pen_color(Color.WHITE)
                    brain.screen.set_cursor(1, 1)
                    brain.screen.print(" [ DRAW CARD ] ")

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
           
            if selected_index < num_playable:
                orig_idx = playable_indices[selected_index]
                played_card = hand.pop(orig_idx)

                print_black(">>> " + p_name + " PLAYED CARD: " + str(played_card) + " <<<")

                # Check if playing down to exactly 1 card triggers UNO (not when playing the last card)
                is_uno = (len(hand) == 1)
                if is_uno:
                    brain.play_sound(SoundType.SIREN)
                    print_black("*** " + p_name + " AUTOMATICALLY CALLED UNO! ***")

                # If a wild card is played, require DECLARE A COLOR confirmation screen
                p_col, _ = parse_card(played_card)
                if p_col == "Wild":
                    declare_color_prompt()

                trigger_card_display(played_card, active_color)

                # Render UNO! header on top of screen when playing down to 1 card
                if is_uno:
                    brain.screen.set_pen_color(Color.YELLOW)
                    brain.screen.set_cursor(1, 1)
                    brain.screen.print("  *** UNO! ***  ")

                execute_robot_movement()
                break
            else:
                played_card = None
                if len(deck) > 0:
                    drawn_cards = draw_cards_from_deck(deck, hand, 1, active_color)
                    print_black(">>> " + p_name + " DREW CARD FROM SHARED DECK: " + str(drawn_cards[0]) + " <<<")
                else:
                    print_black("!!! Shared Draw Deck is empty! !!!")
                break

    # Conceal Transition Screen
    brain.screen.clear_screen()
    brain.screen.set_pen_color(Color.WHITE)
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

def setup_and_play():
    shared_deck = create_uno_deck()
    shuffle_deck(shared_deck)

    players = ["Player"]
    hands = {"Player": []}

    cards_per_player = 7
    for i in range(cards_per_player):
        for player in players:
            if len(shared_deck) > 0:
                hands[player].append(shared_deck.pop())

    # Start match with no initial top card; first card played sets the pile
    top_card = ""
    active_color = "Red"

    print_black("=========================================")
    print_black("=== UNO GAME INITIALIZED ===")
    print_black("Shared Draw Deck Count: " + str(len(shared_deck)) + " cards")
    print_black("Player Hand (" + str(len(hands["Player"])) + " cards): " + str(hands["Player"]))
    print_black("=========================================")
    print_black("")

    current_idx = 0
    skip_next = False

    while True:
        current_player = players[current_idx]

        if skip_next:
            print_black(">>> " + current_player + "'S TURN WAS SKIPPED! <<<")
            handle_skip_screen(current_player, "TURN SKIPPED!")
            skip_next = False
            current_idx = (current_idx + 1) % len(players)
            continue

        top_card, active_color, played_card = display_human_turn(
            current_player, hands[current_player], shared_deck, top_card, active_color
        )

        if len(hands[current_player]) == 0:
            trigger_victory_sequence(current_player)
            break

        if played_card is not None:
            _, val = parse_card(played_card)
            if val == "Skip" or val == "Reverse" or val == "+2" or val == "Wild+4":
                skip_next = True

        current_idx = (current_idx + 1) % len(players)

setup_and_play()