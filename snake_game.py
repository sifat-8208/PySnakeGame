import pygame
import random
import sys


pygame.init()

WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Advanced Snake Game')

clock = pygame.time.Clock()

font = pygame.font.SysFont('arial', 25)

class SnakeGame:
    def __init__(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = "RIGHT"
        self.food = None
        self.score = 0
        self.game_over = False
        self.spawn_food()

    def reset_game(self):
        """Reset the game state."""
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = "RIGHT"
        self.score = 0
        self.game_over = False
        self.spawn_food()

    def spawn_food(self):
        try:
            x_pos = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y_pos = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

            if x_pos is None or y_pos is None:
                print("Error: Generated food position is None.")
                self.food = (100, 100)  
            else:
                self.food = (x_pos, y_pos)
        except Exception as e:
            print(f"Error spawning food: {e}")
            self.food = (100, 100)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.snake_direction == "UP":
            head_y -= BLOCK_SIZE
        elif self.snake_direction == "DOWN":
            head_y += BLOCK_SIZE
        elif self.snake_direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif self.snake_direction == "RIGHT":
            head_x += BLOCK_SIZE

        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

    def check_collisions(self):
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            self.game_over = True
        if (head_x, head_y) in self.snake[1:]:
            self.game_over = True

    def check_food_collision(self):
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        if head_x == food_x and head_y == food_y:
            self.score += 1
            self.snake.append(self.snake[-1]) 
            self.spawn_food()

    def render_snake(self):
        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

    def render_food(self):
        pygame.draw.rect(screen, RED, pygame.Rect(self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))

    def render_score(self):
        score_text = font.render(f"Score: {self.score}", True, BLUE)
        screen.blit(score_text, (10, 10))

    def render_game_over(self):
        game_over_text = font.render("Game Over! Press 'R' to Restart or 'Q' to Quit.", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))

    def run(self):
        """Main game loop."""
        try:
            while not self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_over = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and self.snake_direction != "DOWN":
                            self.snake_direction = "UP"
                        elif event.key == pygame.K_DOWN and self.snake_direction != "UP":
                            self.snake_direction = "DOWN"
                        elif event.key == pygame.K_LEFT and self.snake_direction != "RIGHT":
                            self.snake_direction = "LEFT"
                        elif event.key == pygame.K_RIGHT and self.snake_direction != "LEFT":
                            self.snake_direction = "RIGHT"

                self.move_snake()
                self.check_collisions()
                self.check_food_collision()
                screen.fill(WHITE)
                self.render_snake()
                self.render_food()
                self.render_score()

                if self.game_over:
                    self.render_game_over()

                pygame.display.flip()
                clock.tick(10)

            self.handle_game_over()

        except Exception as e:
            print(f"An error occurred: {e}")
            pygame.quit()
            sys.exit()

    def handle_game_over(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.run() 
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    try:
        game.run()
    except pygame.error as e:
        print(f"Error initializing pygame: {e}")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"Unexpected error: {e}")
        pygame.quit()
        sys.exit()
