import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the game screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window title
pygame.display.set_caption("Snake Game")

import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake properties
snake_segment_size = 20

class Food:
    def __init__(self, screen_w, screen_h, segment_size, snake_body=None):
        self.screen_width = screen_w
        self.screen_height = screen_h
        self.segment_size = segment_size
        self.color = RED
        self.position = [0, 0]
        self.respawn(snake_body) # Initial spawn

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, [self.position[0], self.position[1], self.segment_size, self.segment_size])

    def respawn(self, snake_body=None):
        while True:
            self.position = [
                random.randrange(0, self.screen_width // self.segment_size) * self.segment_size,
                random.randrange(0, self.screen_height // self.segment_size) * self.segment_size
            ]
            if snake_body is None: # For initial spawn before snake exists or if check is not needed
                break
            
            on_snake = False
            for segment in snake_body:
                if self.position[0] == segment[0] and self.position[1] == segment[1]:
                    on_snake = True
                    break
            if not on_snake:
                break


class Snake:
    def __init__(self, start_x, start_y):
        self.body = [[start_x, start_y],
                     [start_x - snake_segment_size, start_y],
                     [start_x - 2 * snake_segment_size, start_y]]
        self.direction = "RIGHT"
        self.color = GREEN
        self.segment_size = snake_segment_size

    def move(self, grow=False):
        head_x, head_y = self.body[0]

        if self.direction == "UP":
            head_y -= self.segment_size
        elif self.direction == "DOWN":
            head_y += self.segment_size
        elif self.direction == "LEFT":
            head_x -= self.segment_size
        elif self.direction == "RIGHT":
            head_x += self.segment_size

        new_head = [head_x, head_y]
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()

    def change_direction(self, new_direction):
        if new_direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, [segment[0], segment[1], self.segment_size, self.segment_size])

    def check_collision_with_food(self, food_position):
        head_x, head_y = self.body[0]
        return head_x == food_position[0] and head_y == food_position[1]

    def is_on_snake(self, position):
        for segment in self.body:
            if position[0] == segment[0] and position[1] == segment[1]:
                return True
        return False

    def check_collision_with_self(self):
        head = self.body[0]
        for segment in self.body[1:]: # Check against body, excluding the head
            if head[0] == segment[0] and head[1] == segment[1]:
                return True
        return False

    def check_collision_with_boundaries(self, screen_w, screen_h):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= screen_w or \
           head_y < 0 or head_y >= screen_h:
            return True
        return False


import sys

# Initialize Pygame font module
pygame.font.init()
score_font = pygame.font.SysFont("arial", 25)
game_over_font = pygame.font.SysFont("arial", 50)
restart_font = pygame.font.SysFont("arial", 30)

# Initialize Pygame mixer
pygame.mixer.init()
eat_sound = None
try:
    eat_sound = pygame.mixer.Sound("eat_sound.wav")
except pygame.error as e:
    print(f"Warning: Could not load sound file 'eat_sound.wav': {e}")


# --- Game State Variables (will be managed by reset_game_state) ---
snake = None
food = None
score = 0
game_over = False
# --- End Game State Variables ---

def reset_game_state():
    global snake, food, score, game_over, screen_width, screen_height, snake_segment_size
    
    snake = Snake(screen_width // 2, screen_height // 2)
    # Pass the new snake's body to Food constructor to avoid spawning on it
    food = Food(screen_width, screen_height, snake_segment_size, snake.body)
    score = 0
    game_over = False

# Initialize game state
reset_game_state()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game_state()
                if event.key == pygame.K_q:
                    running = False
            else:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                if event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                if event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                if event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")

    if not game_over:
        # Game logic
        if snake.check_collision_with_food(food.position):
            snake.move(grow=True)
            score += 1
            if eat_sound:
                eat_sound.play()
            food.respawn(snake.body) 
        else:
            snake.move(grow=False)

        # Check for game over conditions
        if snake.check_collision_with_self() or \
           snake.check_collision_with_boundaries(screen_width, screen_height):
            game_over = True

    # Drawing
    screen.fill(BLACK)  # Fill the screen with black

    if game_over:
        # Display Game Over message
        game_over_msg = game_over_font.render("Game Over", True, WHITE)
        final_score_msg = score_font.render(f"Final Score: {score}", True, WHITE)
        restart_msg = restart_font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
        
        game_over_rect = game_over_msg.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        final_score_rect = final_score_msg.get_rect(center=(screen_width // 2, screen_height // 2))
        restart_rect = restart_msg.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        
        screen.blit(game_over_msg, game_over_rect)
        screen.blit(final_score_msg, final_score_rect)
        screen.blit(restart_msg, restart_rect)
    else:
        if snake: snake.draw(screen)   # Draw the snake
        if food: food.draw(screen)    # Draw the food

        # Display score
        score_text_surface = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text_surface, (10, 10))


    # Update the display
    pygame.display.flip()

    # Control the game's frame rate
    pygame.time.Clock().tick(15)  # Snake speed

pygame.quit()
sys.exit()
