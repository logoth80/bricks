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
RED = (220, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 160, 0)

# Brick dimensions
BRICK_WIDTH = 75
BRICK_HEIGHT = 25

# Paddle dimensions
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 6

# Ball dimensions
BALL_RADIUS = 10
BALL_SPEED = 5.000000

# Bonus dimensions
BONUS_WIDTH = 20
BONUS_HEIGHT = 20
bonus_font = pygame.font.SysFont("Candara", 22, True)
bonus_font_out = pygame.font.SysFont("Candara", 24)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
mouse_x = 1000
# Level definition
level1array = []

level1array.append(
    [
        [0, 1, 1, 1, 2, 2, 1, 1, 1, 0],
        [1, 1, 2, 2, 3, 3, 2, 2, 1, 1],
        [0, 1, 3, 3, 0, 0, 3, 3, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    ]
)


# Brick class
class Brick:
    def __init__(self, x, y, hitpoints):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.hitpoints = hitpoints
        self.maxhitpoints = hitpoints
        if hitpoints == 1:
            self.color = (0, 200, 0)  # Green
        elif hitpoints == 2:
            self.color = (0, 0, 235)  # Blue
        elif hitpoints == 3:
            self.color = (225, 0, 0)  # Red
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
        self.original_width = PADDLE_WIDTH
        self.active_bonuses = []

    def move(self):
        global mouse_x
        mouse_x = mouse_x + min(2 * self.speed, (pygame.mouse.get_pos()[0] - mouse_x) // 1)
        self.rect.x = mouse_x - PADDLE_WIDTH // 2
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

    def apply_bonus(self, bonus_type):
        if bonus_type == "wider":
            self.rect.width = min(self.rect.width + 30, SCREEN_WIDTH)
        elif bonus_type == "faster":
            self.speed += 2

    def remove_bonus(self, bonus_type):
        if bonus_type == "wider":
            self.rect.width = max(self.rect.width - 30, self.original_width)
        elif bonus_type == "faster":
            self.speed = PADDLE_SPEED


# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.dx = random.choice([-BALL_SPEED, BALL_SPEED])
        self.dy = -BALL_SPEED
        self.posx = SCREEN_WIDTH / 2
        self.posy = SCREEN_HEIGHT / 2

    def move(self):
        self.posx += self.dx
        self.posy += self.dy
        self.rect.x = self.posx
        self.rect.y = self.posy

        if self.rect.left <= 0:
            self.dx = abs(self.dx)
        if self.rect.right >= SCREEN_WIDTH:
            self.dx = -abs(self.dx)
        if self.rect.top <= 0:
            self.dy = abs(self.dy)

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def apply_bonus(self, bonus_type):
        global BALL_SPEED
        if bonus_type == "slowdown":
            print(f"temp: {bonus_type}")
            self.dy = self.dy * 0.5
            self.dx = self.dx * 0.5
            BALL_SPEED = BALL_SPEED / 2
        elif bonus_type == "killer":
            print(f"Bonus applied: {bonus_type}")

    def remove_bonus(self, bonus_type):
        global BALL_SPEED
        if bonus_type == "slowdown":
            print(f"temp: {bonus_type}")

            self.dy = self.dy * 2
            self.dx = self.dx * 2
            BALL_SPEED = BALL_SPEED * 2
        elif bonus_type == "killer":
            print(f"Bonus removed: {bonus_type}")


# Bonus class
class Bonus:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BONUS_WIDTH, BONUS_HEIGHT)
        self.type = random.choice(["wider", "faster", "slowdown"])
        self.start_time = None

    def move(self):
        self.rect.y += 3

    def draw(self):
        if self.type == "wider":
            pygame.draw.ellipse(screen, (0, 140, 0), (self.rect[0] - 6, self.rect[1] - 4, self.rect[2] + 12, self.rect[3] + 8))
            # pygame.draw.rect(screen, (0, 200, 0), self.rect)
            text_surface = bonus_font.render("W", True, (0, 255, 0))
            screen.blit(text_surface, (self.rect.centerx - text_surface.get_width() // 2, self.rect.centery - text_surface.get_height() // 2 + 1))

        elif self.type == "faster":
            pygame.draw.ellipse(screen, (140, 0, 0), (self.rect[0] - 6, self.rect[1] - 4, self.rect[2] + 12, self.rect[3] + 8))
            text_surface = bonus_font.render("M", True, (255, 100, 100))
            screen.blit(text_surface, (self.rect.centerx - text_surface.get_width() // 2, self.rect.centery - text_surface.get_height() // 2 + 1))
        elif self.type == "slowdown":
            pygame.draw.ellipse(screen, (0, 0, 120), (self.rect[0] - 6, self.rect[1] - 4, self.rect[2] + 12, self.rect[3] + 8))
            # pygame.draw.rect(screen, BLUE, self.rect)
            text_surface = bonus_font.render("S", True, (120, 120, 255))
            screen.blit(text_surface, (self.rect.centerx - text_surface.get_width() // 2 + 1, self.rect.centery - text_surface.get_height() // 2 + 1))
        else:
            pygame.draw.rect(screen, WHITE, self.rect)


# Create bricks
bricks = []
y_offset = 50
for row in level1array[0]:
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
active_bonuses = []

# Lives/score
lives = 3
score = 0
# Font for UI elements
UIfont = pygame.font.SysFont("Digiface", 36)


# Game loop
running = True
while running:
    current_time = pygame.time.get_ticks()

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
        if ball.dy > 0:
            ball.dy = -abs(ball.dy)
        # Adjust ball's horizontal speed based on where it hits the paddle
        paddle_center = paddle.rect.centerx
        hit_position = (ball.rect.centerx - paddle_center) / (paddle.rect.width / 2)
        print(hit_position, BALL_SPEED, ball.dx)
        # if hit_position < -0.4 or hit_position > 0.4:
        # ball.dx = BALL_SPEED * hit_position + ((1 - abs(hit_position)) * ball.dx)

        print("after:", hit_position, BALL_SPEED, ball.dx)
        if ball.dx > BALL_SPEED:
            ball.dx = BALL_SPEED
        elif ball.dx < -BALL_SPEED:
            ball.dx = -BALL_SPEED
        # ball.dy += -BALL_SPEED / (2 * (1 + abs(hit_position)))

    # Check collision with bricks
    for brick in bricks[:]:
        if brick.hitpoints > 0 and ball.rect.colliderect(brick.rect):
            # Determine collision side
            if abs(ball.rect.bottom - brick.rect.top) <= 8 and ball.dy > 0:
                ball.dy = -abs(ball.dy)
                print("1")
            elif abs(ball.rect.top - brick.rect.bottom) < 8 and ball.dy < 0:
                ball.dy = abs(ball.dy)
                print("2")
            elif abs(ball.rect.right - brick.rect.left) < 8 and ball.dx > 0:
                ball.dx = -abs(ball.dx)
            elif abs(ball.rect.left - brick.rect.right) < 8 and ball.dx < 0:
                ball.dx = abs(ball.dx)

            brick.hit()
            if random.random() < 0.99:  # 10% chance to spawn a bonus
                bonuses.append(Bonus(brick.rect.centerx, brick.rect.centery))
            if brick.hitpoints <= 0:
                bricks.remove(brick)

    # Move bonuses
    for bonus in bonuses[:]:
        bonus.move()
        if bonus.rect.colliderect(paddle.rect):
            bonus.start_time = current_time
            active_bonuses.append(bonus)
            paddle.apply_bonus(bonus.type)
            ball.apply_bonus(bonus.type)

            bonuses.remove(bonus)
        elif bonus.rect.top > SCREEN_HEIGHT:
            bonuses.remove(bonus)

    # Manage active bonuses
    for active_bonus in active_bonuses[:]:
        if current_time - active_bonus.start_time > 30000:  # 10 seconds duration
            ball.remove_bonus(active_bonus.type)
            paddle.remove_bonus(active_bonus.type)
            active_bonuses.remove(active_bonus)

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

    # Draw UI elements (lives, score)
    lives_text = UIfont.render(f"Lives: {lives}", True, WHITE)
    score_text = UIfont.render(f"Score: {score}, {ball.dx:2.2f}, {ball.dy:2.2f}", True, WHITE)
    screen.blit(lives_text, (10, SCREEN_HEIGHT - lives_text.get_height()))
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width(), SCREEN_HEIGHT - score_text.get_height()))

    # Update display
    pygame.display.flip()
    BALL_SPEED += 0.0001
    # Cap frame rate
    clock.tick(60)

pygame.quit()
