import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Brick dimensions
BRICK_WIDTH = 75
BRICK_HEIGHT = 25

# Paddle dimensions
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 6

# Ball dimensions
BALL_RADIUS = 10
BALL_SPEED = 5

# Bonus dimensions
BONUS_WIDTH = 20
BONUS_HEIGHT = 20

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
mouse_x = 1000
# Level definition
level1array = [[0, 1, 1, 1, 2, 2, 1, 1, 1, 0], [1, 1, 2, 2, 3, 3, 2, 2, 1, 1], [0, 1, 3, 3, 0, 0, 3, 3, 1, 0]]


# Brick class
class Brick:
    def __init__(self, x, y, hitpoints):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.hitpoints = hitpoints
        self.maxhitpoints = hitpoints
        if hitpoints == 1:
            self.color = (0, 255, 0)  # Green
        elif hitpoints == 2:
            self.color = (0, 0, 255)  # Blue
        elif hitpoints == 3:
            self.color = (255, 0, 0)  # Red
        self.startr = self.color[0]
        self.startg = self.color[1]
        self.startb = self.color[2]

    def draw(self):
        if self.hitpoints > 0:
            color = (
                int(self.startr * self.hitpoints / self.maxhitpoints),
                int(self.startg * self.hitpoints / self.maxhitpoints),
                int(self.startb * self.hitpoints / self.maxhitpoints),
            )
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)

    def hit(self):
        self.hitpoints -= 1


# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move(self):
        global mouse_x
        mouse_x = mouse_x + min(50, (pygame.mouse.get_pos()[0] - mouse_x) // 1)
        self.rect.x = mouse_x - PADDLE_WIDTH // 2
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)


# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.dx = random.choice([-BALL_SPEED, BALL_SPEED])
        self.dy = -BALL_SPEED

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.dy = -self.dy

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)


# Bonus class
class Bonus:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BONUS_WIDTH, BONUS_HEIGHT)
        self.type = random.choice(["wider", "faster"])

    def move(self):
        self.rect.y += 3

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)


# Create bricks
bricks = []
y_offset = 50
for row in level1array:
    x_offset = 10
    for hitpoints in row:
        if hitpoints > 0:
            bricks.append(Brick(x_offset, y_offset, hitpoints))
        x_offset += BRICK_WIDTH + 5
    y_offset += BRICK_HEIGHT + 5

# Create paddle and ball
paddle = Paddle()
ball = Ball()

# Bonuses
bonuses = []

# Lives
lives = 3

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(BLACK)

    # Move paddle
    paddle.move()

    # Move ball
    ball.move()

    # Check collision with paddle
    if ball.rect.colliderect(paddle.rect):
        ball.dy = -BALL_SPEED

    # Check collision with bricks
    for brick in bricks[:]:
        if brick.hitpoints > 0 and ball.rect.colliderect(brick.rect):
            ball.dy = -ball.dy
            brick.hit()
            if random.random() < 0.1:  # 10% chance to spawn a bonus
                bonuses.append(Bonus(brick.rect.centerx, brick.rect.centery))
            if brick.hitpoints <= 0:
                bricks.remove(brick)

    # Move bonuses
    for bonus in bonuses[:]:
        bonus.move()
        if bonus.rect.colliderect(paddle.rect):
            if bonus.type == "wider":
                paddle.rect.width = min(paddle.rect.width + 30, SCREEN_WIDTH)
            elif bonus.type == "faster":
                paddle.speed += 2
            bonuses.remove(bonus)
        elif bonus.rect.top > SCREEN_HEIGHT:
            bonuses.remove(bonus)

    # Check if ball is lost
    if ball.rect.top > SCREEN_HEIGHT:
        lives -= 1
        ball = Ball()
        if lives <= 0:
            print("Game Over")
            running = False

    # Draw bricks
    for brick in bricks:
        brick.draw()

    # Draw paddle and ball
    paddle.draw()
    ball.draw()

    # Draw bonuses
    for bonus in bonuses:
        bonus.draw()

    # Update display
    pygame.display.flip()

    # Cap frame rate
    clock.tick(60)

pygame.quit()
