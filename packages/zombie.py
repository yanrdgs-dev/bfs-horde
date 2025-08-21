from packages.grid import Grid, LogMixin, Node
import pygame
from collections import deque

class Zombie(LogMixin):
    def __init__(self, x: int, y: int, color: tuple):
        self.x: int = x
        self.y: int = y
        self.color: tuple = color

        self.path: list[Node] = []
        self.path_index: int = 0
        self.last_move_time: int = 0

    def pathfinding_bfs(self, grid: Grid, target: Node) -> None:
        start_node = grid.grid[self.x][self.y]
        queue: deque[Node] = deque([start_node])
        visited: set = {start_node}
        coming_from: dict[Node, Node] = {start_node: None}
        
        path_found = None
        while queue:
            cur_node = queue.popleft()
            
            if cur_node == target:
                self.log(f"Target found at: {cur_node}. Building path...")
                path_found = self.build_path(coming_from, start_node, target)
                break

            for neighbour in cur_node.neighbours:
                if neighbour not in visited and not neighbour.is_obstacle:
                    visited.add(neighbour)
                    queue.append(neighbour)
                    coming_from[neighbour] = cur_node

        if path_found:
            self.path = path_found
        else:
            self.path = []
        self.path_index = 0

    def build_path(self, coming_from: dict[Node, Node], start: Node, target: Node) -> list[Node]:
        path = []
        current_node: Node = target
        
        while current_node != start:
            path.append(current_node)
            current_node = coming_from[current_node]
        
        path.append(start)
        path.reverse()
        self.log(f"Path built.")
        return path
    
    def draw(self, screen, node_width: int, node_height: int):
        zombie_rect = pygame.Rect(self.x * node_width, 
                                  self.y * node_height, 
                                  node_width, node_height)
        pygame.draw.rect(screen, self.color, zombie_rect)