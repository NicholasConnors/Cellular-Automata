import numpy as np
import pygame


class Rule90:
    def __init__(self):
        self.grid_size = int(640 / 4)
        self.cell_size = 4

        # Set all cells to white
        self.grid = np.reshape([False] * (self.grid_size ** 2), (self.grid_size, self.grid_size))

        # Set top row to random
        for i in range(0, self.grid_size):
            self.grid[i][0] = np.random.rand() > 0.5

        self.current_row = 0

    def render(self, screen):
        size = self.cell_size, self.cell_size

        for x, y in np.ndindex((self.grid_size, self.grid_size)):
            # Draw black cells
            if self.grid[x][y]:
                pos = x * self.cell_size, y * self.cell_size
                pygame.draw.rect(screen, (0, 0, 0), (*pos, *size))

    def update(self):
        # Get current row and previous row
        previous_row = self.current_row
        self.current_row += 1

        if self.current_row >= self.grid_size:
            self.current_row = 0

        for i in range(0, self.grid_size):
            # Set the cell in the current row to the exclusive or of its neighbouring values in the previous row
            left = self.grid_size - 1 if i - 1 < 0 else i - 1
            right = 0 if i + 1 >= self.grid_size else i + 1

            value = self.grid[left][previous_row] != self.grid[right][previous_row]
            self.grid[i][self.current_row] = value

        # Clear the grid
        if self.current_row == 0:
            for x in range(0, self.grid_size):
                for y in range(1, self.grid_size):
                    self.grid[x][y] = False

    def input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.reset()

    def reset(self):
        # Set all cells to white
        self.grid = np.reshape([False] * (self.grid_size ** 2), (self.grid_size, self.grid_size))

        # Set top row to random
        for i in range(0, self.grid_size):
            self.grid[i][0] = np.random.rand() > 0.5

        self.current_row = 0
