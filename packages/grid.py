from datetime import datetime
import random

class LogMixin:
    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG @ {timestamp}] {self.__class__.__name__}: {message}")


class Node:
    def __init__(self, x:int , y: int):
        self.x: int = x
        self.y: int = y
        self.is_obstacle: bool = False
        self.neighbours: list[Node] = []
    
    def __repr__(self):
        return f"Node @ ({self.x}, {self.y})"
    

class Grid(LogMixin):
    def __init__(self, size_x: int, size_y: int, obstacle_chance: float=0.3):
        self.size_x: int = size_x
        self.size_y: int = size_y
        self.grid: list[list[Node]] = []
        
        self.create_grid()
        self.generate_obstacles(obstacle_chance)
        self.connect_neighbours()
    
    def create_grid(self):
        for x in range(self.size_x):
            row = []
            for y in range(self.size_y):
                row.append(Node(x, y))
            self.grid.append(row)
        self.log(f"Grid created with size: ({self.size_x}, {self.size_y})")
        
    def generate_obstacles(self, chance: float):
        for x in range(self.size_x):
            for y in range(self.size_y):
                if random.random() < chance:
                    self.grid[x][y].is_obstacle = True
                    self.log(f"Obstacle created at: ({x}, {y})")
         
    def connect_neighbours(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                node = self.grid[x][y]
                if node.is_obstacle:
                    continue
                
                # left node
                if x > 0:
                    neighbour = self.grid[x - 1][y]
                    if not neighbour.is_obstacle:
                        node.neighbours.append(neighbour)
                        
                # right node
                if x < self.size_x - 1:
                    neighbour = self.grid[x + 1][y]
                    if not neighbour.is_obstacle:
                        node.neighbours.append(neighbour)
                        
                # top node
                if y > 0:
                    neighbour = self.grid[x][y - 1]
                    if not neighbour.is_obstacle:
                        node.neighbours.append(neighbour)   
                        
                # bottom node
                if y < self.size_y - 1:
                    neighbour = self.grid[x][y + 1]
                    if not neighbour.is_obstacle:
                        node.neighbours.append(neighbour)
        self.log("Neighbours connected for all nodes.")