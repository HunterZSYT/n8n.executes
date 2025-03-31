import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
SNAKE_COLOR = (0, 255, 0)  # Green
FOOD_COLOR = (255, 0, 0)   # Red
BACKGROUND_COLOR = (0, 0, 0) # Black
TEXT_COLOR = (255, 255, 255) # White
FONT_SIZE = 20

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Snake initial position and movement
snake = [(10, 10)]
snake_direction = (1, 0)  # Initial direction: right (1, 0), left (-1, 0), up (0, -1), down (0, 1)

# Food initial position
food = (random.randint(0, (WIDTH // GRID_SIZE) - 1), random.randint(0, (HEIGHT // GRID_SIZE) - 1))

# Score
score = 0

# Game over flag
game_over = False

# Font for displaying score and game over message
font = pygame.font.Font(None, FONT_SIZE)  # Use default font

# Game clock
clock = pygame.time.Clock()
SNAKE_SPEED = 10  # Adjust this value to change the snake speed


def generate_food():
    """Generates a new food position that is not inside the snake's body."""
    while True:
        new_food = (random.randint(0, (WIDTH // GRID_SIZE) - 1), random.randint(0, (HEIGHT // GRID_SIZE) - 1))
        if new_food not in snake:
            return new_food


def draw_grid():
    """(Optional) Draws a grid on the screen for visual clarity."""
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))


def draw_snake():
    """Draws the snake on the screen."""
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def draw_food():
    """Draws the food on the screen."""
    pygame.draw.rect(screen, FOOD_COLOR, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def display_score():
    """Displays the current score on the screen."""
    text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(text, (5, 5))  # Top-left corner


def game_over_screen():
    """Displays the game over screen with score and instructions."""
    screen.fill(BACKGROUND_COLOR) # Clear the screen

    game_over_text = font.render("Game Over!", True, TEXT_COLOR)
    score_text = font.render(f"Final Score: {score}", True, TEXT_COLOR)
    restart_text = font.render("Press SPACE to restart", True, TEXT_COLOR)

    # Calculate positions to center the texts
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)

    pygame.display.update()

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Exit the program entirely
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_restart = False  # Break out of the loop to restart


def reset_game():
    """Resets the game state to start a new game."""
    global snake, snake_direction, food, score, game_over
    snake = [(10, 10)]
    snake_direction = (1, 0)
    food = generate_food()
    score = 0
    game_over = False


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != (0, 1):
                snake_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                snake_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                snake_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                snake_direction = (1, 0)
            elif event.key == pygame.K_SPACE and game_over: #Restart the game.
                reset_game()

    if not game_over:
        # Update snake position
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])

        # Check for collisions with boundaries
        if (new_head[0] < 0 or new_head[0] >= WIDTH // GRID_SIZE or
            new_head[1] < 0 or new_head[1] >= HEIGHT // GRID_SIZE):
            game_over = True
            continue  # Skip the rest of the loop if game over.

        # Check for self-collision
        if new_head in snake:
            game_over = True
            continue

        snake.insert(0, new_head)  # Add the new head to the snake

        # Check for food collision
        if new_head == food:
            score += 1
            food = generate_food()  # Generate new food
        else:
            snake.pop()  # Remove the tail

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw everything
        #draw_grid()  # Optional: uncomment to draw grid
        draw_snake()
        draw_food()
        display_score()

        # Update the display
        pygame.display.update()

        # Control game speed
        clock.tick(SNAKE_SPEED)
    else:
        # Game over logic (display message, options to restart, etc.)
        game_over_screen()


# Quit Pygame
pygame.quit()
