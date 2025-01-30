import pygame
import sys
from collections import deque
from typing import List, Tuple

# Constants
TILE_SIZE = 80
GRID_COLOR = (200, 200, 200)
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (0, 0, 255)
START_COLOR = (0, 255, 0)
SCREEN_COLOR = (255, 255, 255)
EXPLORE_COLOR = (255, 255, 0)
TEXT_COLOR = (0, 0, 0)

class Maze:
    def __init__(self, grid: List[List[int]], start: Tuple[int, int], screen):
        self.grid = grid
        self.start = start
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.player_pos = start
        self.path = []
        self.explored = []
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.result_text = ""

    def find_path(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = deque([(self.start[0], self.start[1], 0)])
        visited = set()
        visited.add((self.start[0], self.start[1]))

        while queue:
            x, y, steps = queue.popleft()

            # Check if we've reached an exit
            if x == 0 or x == self.rows - 1 or y == 0 or y == self.cols - 1:
                if self.grid[x][y] == 0:  # Ensure it's not a wall
                    self.path = list(visited)
                    self.result_text = f"Exit Found in {steps} steps!"
                    self.draw()
                    return steps

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols and self.grid[nx][ny] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, steps + 1))
                    self.explored.append((nx, ny))
                    self.draw()
                    self.clock.tick(2)

        self.path = list(visited)
        self.result_text = "No Exit Found!"
        self.draw()
        return -1

    def draw(self):
        self.screen.fill(SCREEN_COLOR)
        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                elif (y, x) == self.start:
                    pygame.draw.rect(self.screen, START_COLOR, rect)
                elif (y, x) in self.path:
                    pygame.draw.rect(self.screen, PATH_COLOR, rect)
                elif (y, x) in self.explored:
                    pygame.draw.rect(self.screen, EXPLORE_COLOR, rect)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

        player_rect = pygame.Rect(self.player_pos[1] * TILE_SIZE, self.player_pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, START_COLOR, player_rect)
        
        # Malowanie wyniku w postaci tekstu
        font = pygame.font.SysFont(None, 40)
        text_surf = font.render(self.result_text, True, TEXT_COLOR)
        self.screen.blit(text_surf, (10, self.rows * TILE_SIZE + 10))
        
        pygame.display.flip()

def run_maze_example(grid, start, screen):
    maze = Maze(grid, start, screen)
    maze.find_path()
    maze.draw()
    pygame.display.flip()
    pygame.time.wait(2000)

def main():
    pygame.init()

    # Przykladowe grids dla demonstracii
    grids = [
        [
            [1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 1],
            [1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1]
        ]
    ]
    starts = [(1, 1), (1, 1), (1, 1)]
    
    screen_height = max(len(grid) for grid in grids) * TILE_SIZE + 100
    screen_width = max(len(grid[0]) for grid in grids) * TILE_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Solver")
    clock = pygame.time.Clock()
    running = True

    current_maze_index = 0

    while running:
        screen.fill(SCREEN_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        run_maze_example(grids[current_maze_index], starts[current_maze_index], screen)
        current_maze_index = (current_maze_index + 1) % len(grids)
        
        pygame.display.flip()
        clock.tick(30)
        pygame.time.wait(2000)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
