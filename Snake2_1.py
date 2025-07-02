import pygame
import random
import sys
import time

pygame.init()

# Screen Setup
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake 2.1 - Perfect Grid Edition")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
CYAN = (0, 255, 255)

# Fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 30)

BLOCK_SIZE = 30

def draw_text(text, font, color, pos):
    surface = font.render(text, True, color)
    screen.blit(surface, pos)

def get_playable_area(block_size):
    max_x = (WIDTH // block_size) * block_size
    max_y = (HEIGHT // block_size) * block_size
    return max_x, max_y

def get_grid_dims(block_size):
    max_x, max_y = get_playable_area(block_size)
    return max_x // block_size, max_y // block_size

def get_aligned_pos(block_size, snake, food_positions):
    grid_w, grid_h = get_grid_dims(block_size)
    occupied = set(snake + food_positions)
    while True:
        x = random.randint(0, grid_w - 1) * block_size
        y = random.randint(0, grid_h - 1) * block_size
        if (x, y) not in occupied:
            return (x, y)

def snap_snake_to_grid(snake, block_size):
    return [((x // block_size) * block_size, (y // block_size) * block_size) for (x,y) in snake]

def spawn_all_foods(block_size, snake, extra_food):
    food_positions = []
    for _ in range(1 + extra_food):
        pos = get_aligned_pos(block_size, snake, food_positions)
        food_positions.append(pos)
    return food_positions

def shop_menu(soin, snips, speed, snake_color, block_size, extra_food, score_multiplier):
    block_size_changed = False
    shop_running = True

    soin_options = [
        {"name": "Speed Boost (+2)", "cost": 10},
        {"name": "Change Snake to Blue", "cost": 5},
        {"name": "Change Snake to Yellow", "cost": 5},
        {"name": "Change Snake to Purple", "cost": 7},
        {"name": "Increase Block Size (+5)", "cost": 8},
        {"name": "Decrease Block Size (-5)", "cost": 8},
        {"name": "Decrease Speed (-2)", "cost": 8},
    ]
    snip_options = [
        {"name": "+1 Extra Food on Map", "cost": 2},
        {"name": "+1 Score Multiplier", "cost": 3},
    ]

    all_options = [{"type": "soin", **opt} for opt in soin_options] + \
                  [{"type": "snip", **opt} for opt in snip_options] + \
                  [{"type": "exit", "name": "Exit Shop", "cost": 0}]

    selected = 0

    while shop_running:
        screen.fill(BLACK)
        draw_text("SHOP - Up/Down to select, Enter to buy", font, WHITE, (20, 20))
        draw_text(f"Soins: {soin}", font, YELLOW, (20, 80))
        draw_text(f"Snips: {snips}", font, CYAN, (20, 130))

        for i, option in enumerate(all_options):
            color = WHITE
            if i == selected:
                color = BLUE
            label = f"{option['name']} - Cost: {option['cost']} {'Soins' if option['type']=='soin' else 'Snips' if option['type']=='snip' else ''}"
            draw_text(label, small_font, color, (40, 200 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(all_options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(all_options)
                elif event.key == pygame.K_RETURN:
                    choice = all_options[selected]
                    if choice["type"] == "exit":
                        shop_running = False
                    elif choice["type"] == "soin":
                        if soin >= choice["cost"]:
                            soin -= choice["cost"]
                            if "Speed Boost" in choice["name"]:
                                speed += 2
                            elif "Blue" in choice["name"]:
                                snake_color = BLUE
                            elif "Yellow" in choice["name"]:
                                snake_color = YELLOW
                            elif "Purple" in choice["name"]:
                                snake_color = PURPLE
                            elif "Increase Block Size" in choice["name"] and block_size + 5 <= 80:
                                block_size += 5
                                block_size_changed = True
                            elif "Decrease Block Size" in choice["name"] and block_size - 5 >= 10:
                                block_size -= 5
                                block_size_changed = True
                            elif "Decrease Speed" in choice["name"] and speed - 2 >= 2:
                                speed -= 2
                    elif choice["type"] == "snip":
                        if snips >= choice["cost"]:
                            snips -= choice["cost"]
                            if "+1 Extra Food" in choice["name"]:
                                extra_food += 1
                                block_size_changed = True
                            elif "+1 Score Multiplier" in choice["name"]:
                                score_multiplier += 1

        clock.tick(15)

    return soin, snips, speed, snake_color, block_size, block_size_changed, extra_food, score_multiplier

def game_over_screen(score, soin, snips):
    while True:
        screen.fill(BLACK)
        draw_text("GAME OVER", font, RED, (WIDTH//2 - 200, HEIGHT//2 - 150))
        draw_text(f"Final Score: {score}", font, WHITE, (WIDTH//2 - 200, HEIGHT//2 - 90))
        draw_text(f"Soins Earned: {soin}", font, YELLOW, (WIDTH//2 - 200, HEIGHT//2 - 30))
        draw_text(f"Snips Earned: {snips}", font, CYAN, (WIDTH//2 - 200, HEIGHT//2 + 30))
        draw_text("Press R to Restart or Q to Quit", small_font, WHITE, (WIDTH//2 - 250, HEIGHT//2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    snake_color = GREEN
    speed = 10
    block_size = BLOCK_SIZE

    max_x, max_y = get_playable_area(block_size)
    start_x = (max_x // 2 // block_size) * block_size
    start_y = (max_y // 2 // block_size) * block_size
    snake = [(start_x, start_y)]
    direction = (block_size, 0)
    next_direction = direction

    extra_food = 0
    score_multiplier = 1
    soin = 0
    snips = 0
    score = 0
    food_eaten = 0

    food_positions = spawn_all_foods(block_size, snake, extra_food)

    last_soin_time = time.time()
    last_shop_time = time.time()
    shop_interval = 15

    debug_mode = False
    typed_chars = []

    running = True
    while running:
        clock.tick(speed)
        max_x, max_y = get_playable_area(block_size)

        current_time = time.time()
        if current_time - last_soin_time >= 5:
            soin += 1
            last_soin_time = current_time

        if current_time - last_shop_time >= shop_interval:
            soin, snips, speed, snake_color, block_size, block_size_changed, extra_food, score_multiplier = shop_menu(
                soin, snips, speed, snake_color, block_size, extra_food, score_multiplier)
            last_shop_time = time.time()

            if block_size_changed:
                snake = snap_snake_to_grid(snake, block_size)
                food_positions = spawn_all_foods(block_size, snake, extra_food)

                # Correctly rescale direction based on current heading
                if direction[0] > 0:
                    direction = (block_size, 0)
                    next_direction = (block_size, 0)
                elif direction[0] < 0:
                    direction = (-block_size, 0)
                    next_direction = (-block_size, 0)
                elif direction[1] > 0:
                    direction = (0, block_size)
                    next_direction = (0, block_size)
                elif direction[1] < 0:
                    direction = (0, -block_size)
                    next_direction = (0, -block_size)

                block_size_changed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                new_dir = None
                if event.key in [pygame.K_UP, pygame.K_w]:
                    new_dir = (0, -block_size)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    new_dir = (0, block_size)
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    new_dir = (-block_size, 0)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    new_dir = (block_size, 0)

                if new_dir and (new_dir[0] != -direction[0] or new_dir[1] != -direction[1]):
                    next_direction = new_dir

                if event.unicode.isalpha():
                    typed_chars.append(event.unicode.lower())
                    if len(typed_chars) > 4:
                        typed_chars.pop(0)
                    if ''.join(typed_chars) == "ball":
                        debug_mode = not debug_mode
                        print(f"Debug mode {'ENABLED' if debug_mode else 'DISABLED'}")

        direction = next_direction
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if debug_mode:
            new_head = (new_head[0] % max_x, new_head[1] % max_y)

        snake.insert(0, new_head)

        eaten = False
        for food_pos in food_positions:
            if new_head == food_pos:
                food_positions.remove(food_pos)
                new_food_pos = get_aligned_pos(block_size, snake, food_positions)
                food_positions.append(new_food_pos)

                food_eaten += 1
                score += 1 * score_multiplier
                soin += 1
                if food_eaten % 3 == 0:
                    snips += 1
                eaten = True
                break

        if not eaten:
            snake.pop()

        if not debug_mode:
            if (
                new_head[0] < 0 or new_head[0] >= max_x or
                new_head[1] < 0 or new_head[1] >= max_y or
                new_head in snake[1:]
            ):
                running = False

        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, snake_color, (*segment, block_size, block_size))
        for food_pos in food_positions:
            pygame.draw.rect(screen, RED, (*food_pos, block_size, block_size))

        debug_text = "DEBUG MODE: ON" if debug_mode else "DEBUG MODE: OFF"
        draw_text(debug_text, small_font, CYAN if debug_mode else WHITE, (WIDTH - 300, 10))
        draw_text(f"Score: {score}", font, WHITE, (10, 10))
        draw_text(f"Soins: {soin}", font, YELLOW, (10, 60))
        draw_text(f"Snips: {snips}", font, CYAN, (10, 110))
        draw_text(f"Speed: {speed}", font, WHITE, (10, 160))
        draw_text(f"Block Size: {block_size}", small_font, WHITE, (10, 210))
        draw_text(f"Extra Food on Map: {extra_food}", small_font, WHITE, (10, 260))

        pygame.display.flip()

    game_over_screen(score, soin, snips)

if __name__ == "__main__":
    main()
