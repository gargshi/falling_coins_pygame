import pygame
import random
import sys
import os

# ----------------- Config -----------------
DEBUG = False  # Set True to enable debug prints

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.txt")

# Session state
session = {
    "difficulty": "Easy",
    "sound_on": True,
    "high_score": 0,
    "stg_high_score": 0,  # To track if high score changed during session
}

meta_data = {
    "fallback_sys_font": "Consolas",
    "font_path": "assets/fonts/Electrolize-Regular.ttf"
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

WIDTH, HEIGHT = 380, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Coins Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 223, 0)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
# font = pygame.font.Font(resource_path("assets/fonts/Electrolize-Regular.ttf"), 24) or pygame.font.SysFont("Consolas", 20)
# font = pygame.font.Font(resource_path(meta_data["font_path"]), 24)
# sys_font = pygame.font.SysFont(meta_data["fallback_sys_font"], 20)

# ----------------- Sounds -----------------
pygame.mixer.init()
coin_sound = pygame.mixer.Sound(resource_path("assets/sounds/got_coin.mp3"))
winner_sound = pygame.mixer.Sound(resource_path("assets/sounds/winner.mp3"))
loser_sound = pygame.mixer.Sound(resource_path("assets/sounds/loser.mp3"))


# ----------------- UI Helpers -----------------
# def draw_text(text, x, y, color=WHITE):
#     """Helper to draw centered text"""
#     label = font.render(text, True, color)
#     rect = label.get_rect(center=(x, y))
#     screen.blit(label, rect)
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
        draw_text("Version: 0.1.3", WIDTH // 2, 180, WHITE)
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
    options = ["Resume", "Main Menu"]
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
    player_width, player_height = 40, 20
    player_x = WIDTH // 2
    player_y = HEIGHT - player_height - 10
    player_speed = 7

    coins = []
    score = 0
    # Initialize high score on start game or reseting game
    session["high_score"] = session.get("stg_high_score", 0)

    coin_speed = 4 if session["difficulty"] == "Easy" else 7
    spawn_chance = 20 if session["difficulty"] == "Easy" else 10

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            action = pause_menu()
            if action == "main_menu":
                return

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
                dprint(
                    f"Score={score}, stg High Score={session['stg_high_score']}")
                if score > session["stg_high_score"]:
                    session["high_score"] = score
                    if session["sound_on"] and score == session["stg_high_score"]+1 and session["stg_high_score"] > 0:
                        winner_sound.play()
                coins.remove(coin)
                if session["sound_on"]:
                    coin_sound.play()

        # Remove coins off screen
        coins = [c for c in coins if c[1] < HEIGHT]

        # Draw player
        pygame.draw.rect(screen, WHITE, (player_x, player_y,
                         player_width, player_height))

        # Draw coins
        for coin in coins:
            pygame.draw.circle(screen, GOLD, (coin[0], coin[1]), 10)

        # Draw score
        draw_text(f"Score: {score}", 70, 20)
        draw_text(f"High Score: {session['high_score']}", 100, 50)

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


"""old code"""

# import pygame
# import random
# import sys
# import os

# #settings file
# BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
# SETTINGS_FILE = os.path.join(BASE_DIR, "settings.txt")

# # Global settings
# difficulty = "Easy"
# sound_on = True
# player_high_score = 0
# session={
#     "high_score":0
# }
# def save_settings():
#     with open(SETTINGS_FILE, "w") as f:
#         f.write(f"Difficulty: {difficulty}\n")
#         f.write(f"Sound: {'On' if sound_on else 'Off'}\n")
#         f.write(f"Player High Score: {player_high_score}\n")
# def load_settings():
#     """Load settings from file"""
#     global difficulty, sound_on, player_high_score
#     try:
#         with open(SETTINGS_FILE, "r") as f:
#             lines = f.readlines()
#             difficulty = lines[0].strip().split(": ")[1]
#             sound_on = lines[1].strip().split(": ")[1] == "On"
#             player_high_score = int(lines[2].strip().split(": ")[1])  # Not used in current version
#             session["high_score"]=player_high_score
#             print(f"Loaded settings: Difficulty={difficulty}, Sound={'On' if sound_on else 'Off'}, Player High Score={player_high_score}")
#     except FileNotFoundError:
#         print("Settings file not found. Using default settings.")
#         save_settings()

# # Initialize pygame
# pygame.init()

# #load settings
# load_settings()

# # Screen setup
# WIDTH, HEIGHT = 600, 400
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Falling Coins Game")

# # Colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# GOLD = (255, 223, 0)
# YELLOW = (255, 255, 0)

# # Clock & Font
# clock = pygame.time.Clock()
# font = pygame.font.SysFont("Arial", 25)


# def resource_path(relative_path):
#     """Get absolute path to resource, works for dev and for PyInstaller"""
#     if hasattr(sys, "_MEIPASS"):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)

# # Load sounds
# pygame.mixer.init()
# coin_sound = pygame.mixer.Sound(resource_path("assets/sounds/got_coin.mp3"))  # Ensure you have a coin.wav file
# winner_sound = pygame.mixer.Sound(resource_path("assets/sounds/winner.mp3"))  # Ensure you have a winner.wav file
# loser_sound = pygame.mixer.Sound(resource_path("assets/sounds/loser.mp3"))  # Ensure you have a loser.wav file

# def draw_text(text, x, y, color=WHITE):
#     """Helper to draw centered text"""
#     label = font.render(text, True, color)
#     rect = label.get_rect(center=(x, y))
#     screen.blit(label, rect)


# def main_menu():
#     """Main Menu screen"""
#     options = ["Start Game", "Settings", "Quit"]
#     selected = 0

#     while True:
#         screen.fill(BLACK)

#         draw_text("Falling Coins", WIDTH // 2, 80, YELLOW)

#         for i, option in enumerate(options):
#             color = YELLOW if i == selected else WHITE
#             option_sel=f"<{option}>" if i == selected else option
#             draw_text(option_sel, WIDTH // 2, 180 + i * 40, color)

#         pygame.display.flip()
#         clock.tick(30)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit(); sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     selected = (selected - 1) % len(options)
#                 elif event.key == pygame.K_DOWN:
#                     selected = (selected + 1) % len(options)
#                 elif event.key == pygame.K_RETURN:
#                     if options[selected] == "Start Game":
#                         return "game"
#                     elif options[selected] == "Settings":
#                         return "settings"
#                     elif options[selected] == "Quit":
#                         pygame.quit(); sys.exit()


# def pause_menu():
#     """Pause Menu"""

#     options = ["Resume", "Main Menu"]
#     selected = 0

#     while True:
#         screen.fill(BLACK)
#         draw_text("Paused", WIDTH // 2, 80, YELLOW)

#         for i, option in enumerate(options):
#             color = YELLOW if i == selected else WHITE
#             option_sel=f"<{option}>" if i == selected else option
#             draw_text(option_sel, WIDTH // 2, 180 + i * 40, color)

#         pygame.display.flip()
#         clock.tick(30)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit(); sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     selected = (selected - 1) % len(options)
#                 elif event.key == pygame.K_DOWN:
#                     selected = (selected + 1) % len(options)
#                 elif event.key == pygame.K_RETURN:
#                     if options[selected] == "Resume":
#                         return "resume"
#                     elif options[selected] == "Main Menu":
#                         return "main_menu"
# def settings_menu():
#     """Settings menu"""
#     global difficulty, sound_on
#     options = [f"Difficulty: {difficulty}", f"Sound: {'On' if sound_on else 'Off'}", "Back"]
#     selected = 0

#     while True:
#         screen.fill(BLACK)
#         draw_text("Settings", WIDTH // 2, 80, YELLOW)

#         for i, option in enumerate(options):
#             color = YELLOW if i == selected else WHITE
#             option_sel=f"<{option}>" if i == selected else option
#             draw_text(option_sel, WIDTH // 2, 180 + i * 40, color)

#         pygame.display.flip()
#         clock.tick(30)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit(); sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     selected = (selected - 1) % len(options)
#                 elif event.key == pygame.K_DOWN:
#                     selected = (selected + 1) % len(options)
#                 elif event.key == pygame.K_RETURN:
#                     if options[selected].startswith("Difficulty"):
#                         difficulty = "Hard" if difficulty == "Easy" else "Easy"
#                         options[0] = f"Difficulty: {difficulty}"
#                     elif options[selected].startswith("Sound"):
#                         sound_on = not sound_on
#                         options[1] = f"Sound: {'On' if sound_on else 'Off'}"
#                     elif options[selected] == "Back":
#                         return


# def game_loop():
#     """Main gameplay"""
#     global difficulty, sound_on
#     player_width, player_height = 40, 20
#     player_x = WIDTH // 2
#     player_y = HEIGHT - player_height - 10
#     player_speed = 7

#     coins = []
#     score = 0
#     global player_high_score

#     coin_speed = 4 if difficulty == "Easy" else 7
#     spawn_chance = 20 if difficulty == "Easy" else 10  # lower = more coins

#     running = True
#     while running:
#         screen.fill(BLACK)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit(); sys.exit()

#         # Player input
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_ESCAPE]:
#             action = pause_menu()
#             if action == "main_menu":
#                 return
#         if keys[pygame.K_LEFT] and player_x > 0:
#             player_x -= player_speed
#         if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
#             player_x += player_speed

#         # Add new coin occasionally
#         if random.randint(1, spawn_chance) == 1:
#             coins.append([random.randint(10, WIDTH - 10), 0])

#         # Move coins
#         for coin in coins:
#             coin[1] += coin_speed

#         # Collision detection
#         for coin in coins[:]:
#             if (
#                 player_y < coin[1] + 10
#                 and player_x < coin[0] < player_x + player_width
#             ):
#                 score += 1
#                 print(f"Score: {score}, high score: {player_high_score}")
#                 print(f"Player High Score: {player_high_score}")
#                 print(score>player_high_score)
#                 if player_high_score >= 0 and score > session["high_score"]: #s1 hs0
#                     if sound_on and winner_sound and score == session["high_score"]+1: #s1 hs0
#                         winner_sound.play()
#                     player_high_score = score#s1 hs0
#                     save_settings()

#                 coins.remove(coin)
#                 if sound_on:
#                     coin_sound.play()

#         # Remove coins that fall off
#         coins = [c for c in coins if c[1] < HEIGHT]

#         # Draw player
#         pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

#         # Draw coins
#         for coin in coins:
#             pygame.draw.circle(screen, GOLD, (coin[0], coin[1]), 10)

#         # Draw score
#         draw_text(f"Score: {score}", 70, 20)
#         draw_text(f"High Score: {player_high_score}", 70, 50)

#         pygame.display.flip()
#         clock.tick(60)


# # ---------- Main Game Flow ----------
# while True:
#     action = main_menu()
#     if action == "game":
#         game_loop()
#     elif action == "settings":
#         settings_menu()
#         save_settings()
