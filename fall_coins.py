import pygame
import random
import sys
import os

# ----------------- Config -----------------
DEBUG = False  # Set True to enable debug prints

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.txt")

# Window dimensions
WIDTH, HEIGHT = 380, 640

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 223, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GRAY_DARK = (50, 50, 50)

# Session state
player_stat={
    "lives": 3,
    "score": 0,
    "width": 40,
    "height": 20,
    "speed": 7,
    "color": WHITE
}
coin_stat={
    "size": 8,
    "color": GOLD,
    "speed": 4,
    "easy_speed":4,
    "hard_speed":10,
    "speed_increment":0.5,
    "max_speed":12
}
session = {
    "difficulty": "Easy",
    "sound_on": True,
    "high_score": 0,
    "stg_high_score": 0,  # To track if high score changed during session
    "max_player_width": WIDTH//2,  # Max width player can grow to
    "max_player_speed": 5, #max speed player can grow to 
    "player_width_increment": 5,  # Width increase per 10 points
    "player_stat": player_stat,
    "coin_stat": coin_stat,
    "tmp_chkpt_score":0  # Temporary checkpoint score for in-game tracking
}

meta_data = {
    "fallback_sys_font": "Consolas",
    "font_path": "assets/fonts/Electrolize-Regular.ttf",
    "game_version": "0.1.4"
}

# debug print fn
def dprint(msg):
    if DEBUG:
        print(msg)

# ----------------- Settings -----------------
def save_settings():
    """Save session values to settings.txt"""
    with open(SETTINGS_FILE, "w") as f:
        f.write(f"Difficulty: {session['difficulty']}\n")
        f.write(f"Sound: {'On' if session['sound_on'] else 'Off'}\n")
        f.write(f"High Score: {session['high_score']}\n")


def load_settings():
    """Load session values from settings.txt"""
    try:
        with open(SETTINGS_FILE, "r") as f:
            lines = f.readlines()
            session["difficulty"] = lines[0].strip().split(": ")[1]
            session["sound_on"] = lines[1].strip().split(": ")[1] == "On"
            session["high_score"] = int(lines[2].strip().split(": ")[1])
            session["stg_high_score"] = session["high_score"]
            dprint(f"Loaded settings: {session}")
    except FileNotFoundError:
        dprint("Settings file not found. Using defaults.")
        save_settings()

# ----------------- Helpers -----------------
def resource_path(relative_path):
    """Get absolute path to resource (works for dev and PyInstaller)"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# ----------------- Init Pygame -----------------
pygame.init()
load_settings()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Coins Game")



# ----------------- Fonts -----------------
pygame.font.init()

clock = pygame.time.Clock()

# ----------------- Sounds -----------------
pygame.mixer.init()
coin_sound = pygame.mixer.Sound(resource_path("assets/sounds/got_coin.mp3"))
winner_sound = pygame.mixer.Sound(resource_path("assets/sounds/winner.mp3"))
loser_sound = pygame.mixer.Sound(resource_path("assets/sounds/loser.mp3"))


# ----------------- UI Helpers -----------------
def draw_text(text, x, y, color=WHITE, size=25, font_name=meta_data["font_path"], sys_font_name=meta_data["fallback_sys_font"], use_sysfont=False):
    """
    Draw centered text with adjustable font size.

    Args:
        text (str): Text to render
        x, y (int): Position of text center
        color (tuple): RGB color
        size (int): Font size (default=25)
        font_name (str): System font name (e.g., "Arial") or path to TTF
        use_sysfont (bool): If True, load system font. If False, load TTF from assets.
    """
    if use_sysfont:
        # System font (cross-platform fallback)
        font_obj = pygame.font.SysFont(sys_font_name or "Arial", size)
    else:
        # Bundled font (Google or custom TTF in assets/fonts/)
        font_obj = pygame.font.Font(resource_path(font_name or "assets/fonts/Electrolize-Regular.ttf"), size) or pygame.font.SysFont(sys_font_name, size)

    label = font_obj.render(text, True, color)
    rect = label.get_rect(center=(x, y))
    screen.blit(label, rect)


# ----------------- Menus -----------------
def main_menu():
    """Main Menu screen"""
    options = ["Start Game", "Settings", "Credits", "Quit"]
    selected = 0

    while True:
        screen.fill(BLACK)
        draw_text("Falling Coins", WIDTH // 2, 80, YELLOW)

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            option_sel = f"<{option}>" if i == selected else option
            draw_text(option_sel, WIDTH // 2, 180 + i * 40, color)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected].lower().replace(" ", "_")


def credits_menu():
    """Credits Menu"""
    while True:
        screen.fill(BLACK)
        draw_text("Credits", WIDTH // 2, 80, YELLOW)
        draw_text(f"Version:{meta_data['game_version']} ", WIDTH // 2, 180, WHITE)
        draw_text("Developed by Shivam", WIDTH // 2, 250, WHITE)
        draw_text("Press ESC to return", WIDTH // 2, 400, WHITE, size=18)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


def pause_menu():
    """Pause Menu"""
    options = ["Resume", "Main Menu", "Quit"]
    selected = 0

    while True:
        screen.fill(BLACK)
        draw_text("Paused", WIDTH // 2, 80, YELLOW)

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            option_sel = f"<{option}>" if i == selected else option
            draw_text(option_sel, WIDTH // 2, 180 + i * 40, color)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected].lower().replace(" ", "_")
                elif event.key == pygame.K_ESCAPE:
                    return "resume"


def settings_menu():
    """Settings menu"""
    options = [
        f"Difficulty: {session['difficulty']}",
        f"Sound: {'On' if session['sound_on'] else 'Off'}",
        "Back",
    ]
    selected = 0

    while True:
        screen.fill(BLACK)
        draw_text("Settings", WIDTH // 2, 80, YELLOW)

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            option_sel = f"<{option}>" if i == selected else option
            draw_text(option_sel, WIDTH // 2, 180 + i * 40, color)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected].startswith("Difficulty"):
                        session["difficulty"] = (
                            "Hard" if session["difficulty"] == "Easy" else "Easy"
                        )
                        options[0] = f"Difficulty: {session['difficulty']}"
                    elif options[selected].startswith("Sound"):
                        session["sound_on"] = not session["sound_on"]
                        options[1] = f"Sound: {'On' if session['sound_on'] else 'Off'}"
                    elif options[selected] == "Back":
                        return


# ----------------- Game Loop -----------------
def game_loop():
    """Main gameplay"""
    # global player_width, player_height, player_speed
    player_width = session["player_stat"]["width"]
    player_height = session["player_stat"]["height"]
    player_speed = session["player_stat"]["speed"]
    player_x = WIDTH // 2
    player_y = HEIGHT - player_height - 10

    coins = []
    score = 0
    # Initialize high score on start game or reseting game
    session["high_score"] = session.get("stg_high_score", 0)
    session["coin_stat"]["speed"] = session["coin_stat"]["easy_speed"] if session["difficulty"] == "Easy" else session["coin_stat"]["hard_speed"]
    coin_speed_increment = session["coin_stat"]["speed_increment"]   

    spawn_chance = 30 #if session["difficulty"] == "Easy" else 10

    running = True
    while running:
        screen.fill(GRAY_DARK or GRAY or BLACK) # Dark background for better visibility
        coin_speed = session["coin_stat"]["speed"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Reset player color after timer
            if event.type == pygame.USEREVENT + 1:
                session["player_stat"]["color"] = WHITE
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # stop timer
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                action = pause_menu()
                if action == "main_menu":
                    return
                elif action == "quit":
                    save_settings()
                    pygame.quit()
                    sys.exit()
                elif action == "resume":
                    continue

        # Player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Add new coin occasionally
        if random.randint(1, spawn_chance) == 1:
            coins.append([random.randint(10, WIDTH - 10), 0])

        # Move coins
        for coin in coins:
            coin[1] += coin_speed

        # Collision detection
        for coin in coins[:]:
            if player_y < coin[1] + 10 and player_x < coin[0] < player_x + player_width:
                score += 1                
                if score % 10 == 0 and score > 0 and player_width < session["max_player_width"]:
                    player_width += session["player_width_increment"]  # Increase player width every 10 points
                    player_speed = min(session["max_player_speed"], player_speed + 0.5)  # increase speed slightly, min 5
                    session["player_stat"]["width"] = player_width
                    session["player_stat"]["speed"] = player_speed
                    session["coin_stat"]["speed"] = min(session["coin_stat"]["max_speed"], coin_speed + coin_speed_increment)
                    session["player_stat"]["color"] = GREEN
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # Reset color after 1 second
                    
                dprint(f"Score={score}, stg High Score={session['stg_high_score']}")
                if score > session["stg_high_score"]:
                    session["high_score"] = score
                    if session["sound_on"] and score == session["stg_high_score"]+1 and session["stg_high_score"] > 0:                        
                        session["player_stat"]["color"] = GOLD                        
                        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # Reset color after 1 second                        
                        winner_sound.play()
                coins.remove(coin)
                if session["sound_on"]:
                    coin_sound.play()

        # Remove coins off screen
        coins = [c for c in coins if c[1] < HEIGHT]

        # Draw player
        # pygame.draw.rect(screen, session["player_stat"]["color"], (player_x, player_y,
        #                  player_width, player_height))
        # After drawing player rect
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        pygame.draw.rect(screen, session["player_stat"]["color"], player_rect)

        text_color = BLACK if session["player_stat"]["color"] in (WHITE, GOLD, GREEN) else WHITE
        player_label = session["player_stat"].get("label", f"{score}")

        # Use draw_text
        draw_text(player_label, player_rect.centerx, player_rect.centery, color=text_color, size=15)

        # Draw coins
        for coin in coins:
            pygame.draw.circle(screen, session["coin_stat"]["color"], (coin[0], coin[1]), session["coin_stat"]["size"])

        # Draw score
        draw_text(f"Score: {score}", 70, 20)
        draw_text(f"High Score: {session['high_score']}", 100, 50)
        # draw_text(f"{coin_speed} Coin Speed: {session['coin_stat']['speed']}", 130, 80)

        pygame.display.flip()
        clock.tick(60)

    save_settings()


# ----------------- Main Flow -----------------
while True:
    action = main_menu()
    if action == "start_game":
        game_loop()
        save_settings()  # Save high score after each game
    elif action == "settings":
        settings_menu()
        save_settings()
    elif action == "credits":
        credits_menu()
    elif action == "quit":
        save_settings()
        pygame.quit()
        sys.exit()