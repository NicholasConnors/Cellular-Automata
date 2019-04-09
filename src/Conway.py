import numpy as np
import pygame


class Conway:
    def __init__(self):
        self.grid_size = 64
        self.cell_size = 10

        self.grid = np.reshape([False] * (self.grid_size**2), (self.grid_size, self.grid_size))
        self.running = False

    def render(self, screen):
        for x, y in np.ndindex((self.grid_size, self.grid_size)):
            # Draw "alive" cells
            if self.grid[x][y]:
                pos = x * self.cell_size, y * self.cell_size
                size = self.cell_size, self.cell_size
                pygame.draw.rect(screen, (0, 0, 0), (*pos, *size))

    def update(self):
        if not self.running:
            return

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

                if self.grid[n_x][n_y]:
                    neighbours += 1

            value = False
            # RULE 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation
            # RULE 3: Any live cell with more than three live neighbours dies, as if by overpopulation
            if self.grid[x][y] and (neighbours < 2 or neighbours > 3):
                value = False
            # RULE 2: Any live cell with two or three live neighbours lives on to the next generation
            # RULE 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
            elif self.grid[x][y] or (not self.grid[x][y] and neighbours == 3):
                value = True

            new_grid.append(value)

        self.grid = np.reshape(new_grid, (self.grid_size, self.grid_size))

    def input(self, event):
        if not self.running and event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            x = int(x_mouse / self.cell_size)
            y = int(y_mouse / self.cell_size)

            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                self.grid[x][y] = not self.grid[x][y]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not self.running:
                    self.running = True
                else:
                    self.running = False
                    self.grid = np.reshape([False] * (self.grid_size ** 2), (self.grid_size, self.grid_size))
            if event.key == pygame.K_r:
                self.running = False
                # Randomly make some cells
                self.grid = [False] * (self.grid_size ** 2)
                for i in range(self.grid_size ** 2):
                    random = np.random.randint(6)
                    if random == 2:
                        self.grid[i] = True

                self.grid = np.reshape(self.grid, (self.grid_size, self.grid_size))
