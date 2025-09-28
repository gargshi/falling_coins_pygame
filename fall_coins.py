import pygame
import random
import sys
import os

#settings file
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.txt")

# Global settings
difficulty = "Easy"
sound_on = True
def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        f.write(f"Difficulty: {difficulty}\n")
        f.write(f"Sound: {'On' if sound_on else 'Off'}\n")
def load_settings():
    """Load settings from file"""
    global difficulty, sound_on
    try:
        with open(SETTINGS_FILE, "r") as f:
            lines = f.readlines()
            difficulty = lines[0].strip().split(": ")[1]
            sound_on = lines[1].strip().split(": ")[1] == "On"
    except FileNotFoundError:
        save_settings()

# Initialize pygame
pygame.init()

#load settings
load_settings()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Coins Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 223, 0)
YELLOW = (255, 255, 0)

# Clock & Font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)



def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Load sounds
pygame.mixer.init()
coin_sound = pygame.mixer.Sound(resource_path("assets/sounds/got_coin.mp3"))  # Ensure you have a coin.wav file
winner_sound = pygame.mixer.Sound(resource_path("assets/sounds/winner.mp3"))  # Ensure you have a winner.wav file
loser_sound = pygame.mixer.Sound(resource_path("assets/sounds/loser.mp3"))  # Ensure you have a loser.wav file





def draw_text(text, x, y, color=WHITE):
    """Helper to draw centered text"""
    label = font.render(text, True, color)
    rect = label.get_rect(center=(x, y))
    screen.blit(label, rect)


def main_menu():
    """Main Menu screen"""
    options = ["Start Game", "Settings", "Quit"]
    selected = 0

    while True:
        screen.fill(BLACK)

        draw_text("Falling Coins", WIDTH // 2, 80, YELLOW)

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            draw_text(option, WIDTH // 2, 180 + i * 40, color)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Start Game":
                        return "game"
                    elif options[selected] == "Settings":
                        return "settings"
                    elif options[selected] == "Quit":
                        pygame.quit(); sys.exit()


def pause_menu():    
    """Pause Menu"""

    options = ["Resume", "Main Menu"]
    selected = 0

    while True:
        screen.fill(BLACK)
        draw_text("Paused", WIDTH // 2, 80, YELLOW)

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            draw_text(option, WIDTH // 2, 180 + i * 40, color)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Resume":
                        return "resume"
                    elif options[selected] == "Main Menu":
                        return "main_menu"
def settings_menu():
    """Settings menu"""
    global difficulty, sound_on
    options = [f"Difficulty: {difficulty}", f"Sound: {'On' if sound_on else 'Off'}", "Back"]
    selected = 0

    while True:
        screen.fill(BLACK)
        draw_text("Settings", WIDTH // 2, 80, YELLOW)

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            option_sel=f"<{option}>" if i == selected else option
            draw_text(option_sel, WIDTH // 2, 180 + i * 40, color)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected].startswith("Difficulty"):
                        difficulty = "Hard" if difficulty == "Easy" else "Easy"
                        options[0] = f"Difficulty: {difficulty}"
                    elif options[selected].startswith("Sound"):
                        sound_on = not sound_on
                        options[1] = f"Sound: {'On' if sound_on else 'Off'}"
                    elif options[selected] == "Back":
                        return


def game_loop():
    """Main gameplay"""
    global difficulty, sound_on
    player_width, player_height = 40, 20
    player_x = WIDTH // 2
    player_y = HEIGHT - player_height - 10
    player_speed = 7

    coins = []
    score = 0

    coin_speed = 4 if difficulty == "Easy" else 7
    spawn_chance = 20 if difficulty == "Easy" else 10  # lower = more coins

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # Player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            action = pause_menu()
            if action == "main_menu":
                return
            elif action == "resume":
                continue          
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
            if (
                player_y < coin[1] + 10
                and player_x < coin[0] < player_x + player_width
            ):
                score += 1
                coins.remove(coin)
                if sound_on:
                    coin_sound.play()

        # Remove coins that fall off
        coins = [c for c in coins if c[1] < HEIGHT]

        # Draw player
        pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

        # Draw coins
        for coin in coins:
            pygame.draw.circle(screen, GOLD, (coin[0], coin[1]), 10)

        # Draw score
        draw_text(f"Score: {score}", 70, 20)

        pygame.display.flip()
        clock.tick(60)


# ---------- Main Game Flow ----------
while True:
    action = main_menu()
    if action == "game":
        game_loop()
    elif action == "settings":
        settings_menu()
        save_settings()
