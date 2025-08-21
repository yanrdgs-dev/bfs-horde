from packages.grid import LogMixin, Grid
import pygame

class Player(LogMixin):
    def __init__(self, x: int, y: int, color: tuple, grid: Grid):
        self.x = x
        self.y = y
        self.color = color
        self.last_move_time = 0
        self.move_cooldown = 700
        self.grid: Grid = grid

    def move(self, grid_width, grid_height, dx=0, dy=0, current_time=0):
        
        if current_time - self.last_move_time < self.move_cooldown:
            remaining_time = self.move_cooldown - (current_time - self.last_move_time)
            self.log(f"Player can't move! Wait {remaining_time} ms.")
            return False
        
        self.last_move_time = current_time
        next_x = self.x + dx
        next_y = self.y + dy
        
        if 0 <= next_x < grid_width and 0 <= next_y < grid_height:
            if not self.grid.grid[next_x][next_y].is_obstacle:
                self.x = next_x
                self.y = next_y
                self.log(f"Player moved to: ({self.x}, {self.y})")
                return True
        return False

    def draw(self, screen, node_width: int, node_height: int):
        player_rect = pygame.Rect(self.x * node_width, 
                                  self.y * node_height, 
                                  node_width, node_height)
        pygame.draw.rect(screen, self.color, player_rect)
        # self.log(f"Player drawn at: ({self.x}, {self.y})")