import pygame
import random
import sys
import time

pygame.init()

# Screen Setup
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake 2.1 - Smarter Boss Edition")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)

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
    return [((x // block_size) * block_size, (y // block_size) * block_size) for (x, y) in snake]

def spawn_all_foods(block_size, snake, extra_food):
    food_positions = []
    for _ in range(1 + extra_food):
        pos = get_aligned_pos(block_size, snake, food_positions)
        food_positions.append(pos)
    return food_positions

def boss_fight(snake, block_size, speed, sointes):
    boss_color = PINK
    max_x, max_y = get_playable_area(block_size)
    grid_w, grid_h = get_grid_dims(block_size)
    
    boss_pos = (random.randint(0, grid_w - 1) * block_size,
                random.randint(0, grid_h - 1) * block_size)
    target_pos = (random.randint(0, grid_w - 1) * block_size,
                  random.randint(0, grid_h - 1) * block_size)
    
    start_time = time.time()
    boss_duration = 30
    clock = pygame.time.Clock()

    direction = (block_size, 0)

    while True:
        clock.tick(speed)
        screen.fill(BLACK)

        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, block_size, block_size))
        pygame.draw.rect(screen, boss_color, (*boss_pos, block_size, block_size))

        time_left = max(0, int(boss_duration - (time.time() - start_time)))
        draw_text(f"Boss Fight! Catch the Boss! Time Left: {time_left}s", small_font, WHITE, (20, 20))
        draw_text(f"Sointes: {sointes}", small_font, ORANGE, (20, 60))

        pygame.display.flip()

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
                if new_dir and (len(snake) < 2 or new_dir != (-direction[0], -direction[1])):
                    direction = new_dir

        head_x, head_y = snake[0]
        new_head = ((head_x + direction[0]) % max_x, (head_y + direction[1]) % max_y)
        snake.insert(0, new_head)
        snake.pop()

        if new_head == boss_pos:
            sointes += 5
            return sointes

        bx, by = boss_pos
        tx, ty = target_pos

        if bx < tx:
            bx += block_size
        elif bx > tx:
            bx -= block_size
        elif by < ty:
            by += block_size
        elif by > ty:
            by -= block_size
        else:
            target_pos = (random.randint(0, grid_w - 1) * block_size,
                          random.randint(0, grid_h - 1) * block_size)

        boss_pos = (bx % max_x, by % max_y)

        if time.time() - start_time > boss_duration:
            return sointes
def main(sointes=0, perm_snip_multi=0, perm_sointe_multi=0, boss_unlocked=True):
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

        if time.time() - last_soin_time >= 5:
            soin += 1
            last_soin_time = time.time()

        if time.time() - last_shop_time >= shop_interval:
            soin, snips, sointes, speed, snake_color, block_size, block_size_changed, extra_food, score_multiplier, perm_snip_multi, perm_sointe_multi, boss_unlocked = shop_menu(
                soin, snips, sointes, speed, snake_color, block_size, extra_food, score_multiplier, perm_snip_multi, perm_sointe_multi, boss_unlocked
            )
            last_shop_time = time.time()

            if block_size_changed:
                snake = snap_snake_to_grid(snake, block_size)
                food_positions = spawn_all_foods(block_size, snake, extra_food)
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
                        print("KEKW Debug Mode:", debug_mode)

        direction = next_direction
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if debug_mode:
            new_head = (new_head[0] % max_x, new_head[1] % max_y)
        snake.insert(0, new_head)

        eaten = False
        for food_pos in food_positions:
            if new_head == food_pos:
                food_positions.remove(food_pos)
                food_positions.append(get_aligned_pos(block_size, snake, food_positions))
                food_eaten += 1
                score += 1 * score_multiplier
                soin += 1
                if food_eaten % 3 == 0:
                    snips += 1 * (perm_snip_multi + 1)
                eaten = True
                break

        if not eaten:
            snake.pop()

        if score >= 100:
            if boss_unlocked:
                sointes = boss_fight(snake, block_size, speed, sointes)
                main(sointes, perm_snip_multi, perm_sointe_multi, boss_unlocked)
                return

        if not debug_mode:
            if (
                new_head[0] < 0 or new_head[0] >= max_x or
                new_head[1] < 0 or new_head[1] >= max_y or
                new_head in snake[1:]
            ):
                print("PEPEGA Game Over")
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, snake_color, (*segment, block_size, block_size))
        for food_pos in food_positions:
            pygame.draw.rect(screen, RED, (*food_pos, block_size, block_size))

        draw_text(f"Score: {score}", font, WHITE, (10, 10))
        draw_text(f"Soins: {soin}", font, YELLOW, (10, 60))
        draw_text(f"Snips: {snips}", font, CYAN, (10, 110))
        draw_text(f"Sointes: {sointes}", font, ORANGE, (10, 160))

        pygame.display.flip()

if __name__ == "__main__":
    print("POGGERS Starting Snake 2.1")
    main()
