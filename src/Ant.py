import numpy as np
import pygame


class Ant:
    def __init__(self):
        self.grid_size = 64
        self.cell_size = 10

        # Place ant in the center of the grid
        self.ant = (int(self.grid_size / 2), int(self.grid_size / 2))

        # Direction the ant is facing. 0 - left; 1 - up; 2 - right; 3 - down
        self.ant_dir = 0

        # Set all cells to white
        self.grid = np.reshape([False] * (self.grid_size ** 2), (self.grid_size, self.grid_size))

    def render(self, screen):
        size = self.cell_size, self.cell_size

        for x, y in np.ndindex((self.grid_size, self.grid_size)):
            # Draw black cells
            if self.grid[x][y]:
                pos = x * self.cell_size, y * self.cell_size
                pygame.draw.rect(screen, (0, 0, 0), (*pos, *size))

        # Draw the ant
        x, y = self.ant
        pos = x * self.cell_size + 2, y * self.cell_size + 2
        pygame.draw.rect(screen, (255, 0, 0), (*pos, self.cell_size - 4, self.cell_size - 4))

    def update(self):
        x, y = self.ant

        # If the ant has escaped, reset
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            self.reset()
            return

        # At a white square turn to the right
        if not self.grid[x][y]:
            self.ant_dir += 1
        # At a black square turn to the left
        if self.grid[x][y]:
            self.ant_dir -= 1

        # Keep dir between 0 and 3
        self.ant_dir = self.ant_dir % 4

        # Flip grid colour
        self.grid[x][y] = not self.grid[x][y]

        # Move forward one unit

        # Go left
        if self.ant_dir == 0:
            x -= 1

        # Go up
        elif self.ant_dir == 1:
            y -= 1

        # Go right
        elif self.ant_dir == 2:
            x += 1

        # Go down
        elif self.ant_dir == 3:
            y += 1

        self.ant = x, y

    def input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.reset()

    def reset(self):
        # Place ant in the center of the grid
        self.ant = (int(self.grid_size / 2), int(self.grid_size / 2))

        # Direction the ant is facing. 0 - left; 1 - up; 2 - right; 3 - down
        self.ant_dir = 0

        # Set all cells to white
        self.grid = np.reshape([False] * (self.grid_size**2), (self.grid_size, self.grid_size))
