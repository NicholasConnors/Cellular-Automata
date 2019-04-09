import numpy as np
import pygame
from enum import Enum


class Cell(Enum):
    ALIVE = 0
    DYING = 1
    DEAD = 2


class Brian:
    def __init__(self):
        self.grid_size = 64
        self.cell_size = 10

        # Randomly make some cells
        self.grid = [Cell.DEAD] * (self.grid_size**2)
        for i in range(self.grid_size**2):
            random = np.random.randint(6)
            if random == 2:
                self.grid[i] = Cell.ALIVE

        self.grid = np.reshape(self.grid, (self.grid_size, self.grid_size))

    def render(self, screen):
        for x, y in np.ndindex((self.grid_size, self.grid_size)):
            # Draw "alive" and "dying" cells
            if self.grid[x][y] != Cell.DEAD:
                pos = x * self.cell_size, y * self.cell_size
                size = self.cell_size, self.cell_size
                colour = (0, 0, 0) if self.grid[x][y] == Cell.ALIVE else (60, 120, 255)
                pygame.draw.rect(screen, colour, (*pos, *size))

    def update(self):
        new_grid = []
        for x, y in np.ndindex((self.grid_size, self.grid_size)):
            # Count number of neighbour cells
            neighbours = 0
            for dx, dy in (np.ndindex(3, 3)):
                if dx == dy == 1:
                    continue

                # Get neighbour grid position
                n_x = x + dx - 1
                n_y = y + dy - 1

                # Torus
                if n_x < 0:
                    n_x += self.grid_size
                if n_y < 0:
                    n_y += self.grid_size
                if n_x >= self.grid_size:
                    n_x -= self.grid_size
                if n_y >= self.grid_size:
                    n_y -= self.grid_size

                if self.grid[n_x][n_y] == Cell.ALIVE:
                    neighbours += 1

            # Rule 3: Dying cells go to dead cells
            state = Cell.DEAD

            # RULE 1: A cell turns on if it was off but has exactly two neighbours that are on
            if self.grid[x][y] == Cell.DEAD and neighbours == 2:
                state = Cell.ALIVE

            # RULE 2: Alive cells go to dying cells
            if self.grid[x][y] == Cell.ALIVE:
                state = Cell.DYING

            new_grid.append(state)

        self.grid = np.reshape(new_grid, (self.grid_size, self.grid_size))

    def input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.reset()

    def reset(self):
        # Randomly make some cells
        self.grid = [Cell.DEAD] * (self.grid_size**2)
        for i in range(self.grid_size**2):
            random = np.random.randint(6)
            if random == 2:
                self.grid[i] = Cell.ALIVE

        self.grid = np.reshape(self.grid, (self.grid_size, self.grid_size))
