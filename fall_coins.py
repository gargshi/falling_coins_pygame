import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Coins Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 223, 0)

# Game clock
clock = pygame.time.Clock()

# Player
player_width = 40
player_height = 10
player_x = WIDTH // 2
player_y = HEIGHT - player_height - 10
player_speed = 7

# Coins
coin_radius = 10
coins = []
coin_speed = 4

# Score
score = 0
font = pygame.font.SysFont("Arial", 24)

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Add new coin occasionally
    if random.randint(1, 20) == 1:
        coins.append([random.randint(coin_radius, WIDTH - coin_radius), 0])

    # Move coins
    for coin in coins:
        coin[1] += coin_speed

    # Collision detection
    for coin in coins[:]:
        if (
            player_y < coin[1] + coin_radius
            and player_x < coin[0] < player_x + player_width
        ):
            score += 1
            coins.remove(coin)

    # Remove coins that fall off screen
    coins = [c for c in coins if c[1] < HEIGHT]

    # Drawing
    screen.fill(BLACK)

    # Draw player
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

    # Draw coins
    for coin in coins:
        pygame.draw.circle(screen, GOLD, (coin[0], coin[1]), coin_radius)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)  # 60 FPS
