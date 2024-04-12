import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60

# Player properties
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 40
PLAYER_SPEED = 5

# Bullet properties
BULLET_WIDTH, BULLET_HEIGHT = 5, 15
BULLET_SPEED = 7

# Enemy properties
ENEMY_WIDTH, ENEMY_HEIGHT = 60, 40
ENEMY_SPEED = 3

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fighter Plane")
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.color = RED
        self.rect = pygame.Rect(WIDTH // 2 - self.width // 2, HEIGHT - self.height - 20, self.width, self.height)
        self.vel = 0

    def update(self):
        self.vel = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vel = PLAYER_SPEED
        self.rect.x += self.vel
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.color = WHITE
        self.rect = pygame.Rect(x - self.width // 2, y - self.height, self.width, self.height)

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.color = WHITE
        self.rect = pygame.Rect(random.randrange(WIDTH - self.width), random.randrange(-100, -40), self.width, self.height)
        self.vel_y = ENEMY_SPEED

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.width)
            self.rect.y = random.randrange(-100, -40)

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

score = 0
font = pygame.font.Font(None, 36)
level_complete = False

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Update
    all_sprites.update()

    # Check for bullet-enemy collision
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        score += 1

    # Check for player-enemy collision
    hits = pygame.sprite.spritecollide(player, enemies, True)
    if hits:
        running = False

    # Scroll enemies
    if len(enemies) < 5:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Draw
    screen.fill(BLACK)
    for sprite in all_sprites:
        pygame.draw.rect(screen, sprite.color, sprite.rect)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    if score >= 200:
        level_complete = True
        level_complete_text = font.render("Level Complete!", True, WHITE)
        screen.blit(level_complete_text, (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    # Restart the game if level complete
    if level_complete:
        pygame.time.wait(2000)  # Wait for 2 seconds
        level_complete = False
        score = 0

pygame.quit()
sys.exit()
