import pygame
from packages.grid import Grid, LogMixin, Node
from packages.zombie import Zombie
from packages.player import Player
import random
pygame.init()

# game consts
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NODE_WIDTH = 40
NODE_HEIGHT = 40
COLUMNS = SCREEN_WIDTH // NODE_WIDTH
ROWS = SCREEN_HEIGHT // NODE_HEIGHT
START_POS_X = COLUMNS // 2
START_POS_Y = ROWS // 2
GAME_OVER_FONT = pygame.font.Font(None, 74)

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (40, 40, 40)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
OBSTACLE_COLOR = (128, 128, 128)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Pathfinding Simulation")

def draw_grid(grid):
    for x in range(0, SCREEN_WIDTH, NODE_WIDTH):
        pygame.draw.line(SCREEN, GREY, (x, 0), (x, SCREEN_HEIGHT))

    for y in range(0, SCREEN_HEIGHT, NODE_HEIGHT):
        pygame.draw.line(SCREEN, GREY, (0, y), (SCREEN_WIDTH, y))

    for x in range(grid.size_x):
        for y in range(grid.size_y):
            if grid.grid[x][y].is_obstacle:
                obstacle_rect = pygame.Rect(x * NODE_WIDTH, y * NODE_HEIGHT, NODE_WIDTH, NODE_HEIGHT)
                pygame.draw.rect(SCREEN, OBSTACLE_COLOR, obstacle_rect)

grid: Grid = Grid(COLUMNS, ROWS, obstacle_chance=0.25)
player: Player = Player(START_POS_X, START_POS_Y, BLUE, grid)
grid.grid[START_POS_X][START_POS_Y].is_obstacle = False
zombies: list[Zombie] = []
for i in range(3):
    while True:
        x = random.randint(0, COLUMNS - 1)
        y = random.randint(0, ROWS - 1)
        if x != START_POS_X or y != START_POS_Y:
            break
    if x == START_POS_X and y == START_POS_Y:
        continue
    zombie: Zombie = Zombie(x, y, GREEN)
    grid.grid[zombie.x][zombie.y].is_obstacle = False
    zombies.append(zombie)
    
game_state: str = "running"
playing: bool = True
while playing:
    if game_state == "running":
        player_moved = False
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player_moved = player.move(dx=-1, dy=0, grid_width=COLUMNS, grid_height=ROWS, current_time=current_time)
                if event.key == pygame.K_d:
                    player_moved = player.move(dx=1, dy=0, grid_width=COLUMNS, grid_height=ROWS, current_time=current_time)
                if event.key == pygame.K_w:
                    player_moved = player.move(dx=0, dy=-1, grid_width=COLUMNS, grid_height=ROWS, current_time=current_time)
                if event.key == pygame.K_s:
                    player_moved = player.move(dx=0, dy=1, grid_width=COLUMNS, grid_height=ROWS, current_time=current_time)
        if player_moved:
            target_node: Node = grid.grid[player.x][player.y]
            for zombie in zombies:
                zombie.pathfinding_bfs(grid, target_node)
        
        current_time = pygame.time.get_ticks()
        
        for zombie in zombies:
            if zombie.path and current_time - zombie.last_move_time > 500:
                zombie.last_move_time = current_time
                if zombie.path_index < len(zombie.path):
                    next_node = zombie.path[zombie.path_index]
                    zombie.x, zombie.y = next_node.x, next_node.y
                    zombie.path_index += 1
        
            for zombie in zombies:
                if zombie.x == player.x and zombie.y == player.y:
                    game_state = "game_over"
                    print("Game Over! You were caught by a zombie!")
                    break
        SCREEN.fill(BLACK)
        draw_grid(grid)
        
        player.draw(SCREEN, NODE_WIDTH, NODE_HEIGHT)
        for zombie in zombies:
            zombie.draw(SCREEN, NODE_WIDTH, NODE_HEIGHT)
        pygame.display.flip()

    if game_state == "game_over":
        SCREEN.fill(WHITE)
        game_over_text = GAME_OVER_FONT.render("YOU DIED!", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(game_over_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        playing = False

pygame.quit()
