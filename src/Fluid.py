import numpy as np
import pygame

max_value = 1.0
min_value = 0.005
max_compression = 0.2
min_flow = 0.01
max_flow = 4.0
show_fluid_count = False


class Cell:
    def __init__(self, fluid, dynamic=True):
        self.fluid = fluid
        self.dynamic = dynamic
        self.falling = False
        self.d_fluid = 0


def calculate_vertical_flow(source_fluid, destination):
    total = source_fluid + destination.fluid

    value = max_value
    if total > max_value:
        value = (1 + total*max_compression) / (1 + max_compression)
    if total >= (2 * max_value + max_compression):
        value = (total + max_compression) / 2

    return value


class Fluid:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 12)

        self.grid_size = 32
        self.cell_size = 20

        self.grid = [Cell(0) for i in range(0, self.grid_size**2)]
        self.grid = np.reshape(self.grid, (self.grid_size, self.grid_size))
        # Line at bottom for screen
        for i in range(0, self.grid_size):
            self.grid[i, self.grid_size - 1].dynamic = False

        self.adding_block = False

    def render(self, screen):
        for x, y in np.ndindex(self.grid_size, self.grid_size):
            cell = self.grid[x, y]

            # Apply changes and then reset
            cell.fluid += cell.d_fluid
            cell.d_fluid = 0

            # Check against min value
            if cell.fluid < min_value:
                cell.fluid = 0

            h = np.amin((cell.fluid, 1)) if cell.dynamic and not cell.falling else 1
            if cell.falling:
                h = 1
            pos = x * self.cell_size, (y + 1 - h) * self.cell_size
            shape = self.cell_size, self.cell_size * np.amin((h + 0.1, 1))
            colour = (255, 0, 0)

            # Reset falling
            cell.falling = False

            if not cell.dynamic:
                colour = (0, 0, 0)
            elif cell.fluid == 0:
                colour = (255, 255, 255)
            elif cell.dynamic:
                # Base lightness of the blue off of cell "fullness"
                light_blue = np.array([155, 225, 255])
                dark_blue = np.array([0, 90, 128])
                blue = np.array([20, 184, 255])
                darkest_blue = np.array([0, 8, 32])

                # If pressurized, darken colour
                if cell.fluid >= 10:
                    colour = darkest_blue
                elif cell.fluid >= 4:
                    percentage = 1 - (cell.fluid - 4)/6.0
                    colour = darkest_blue * (1 - percentage) + dark_blue * percentage
                elif cell.fluid > 2:
                    percentage = 1 - (cell.fluid - 2)/2.0
                    colour = dark_blue * (1 - percentage) + blue * percentage
                else:
                    percentage = 1 - (cell.fluid/2.0)
                    colour = blue * (1 - percentage) + light_blue * percentage

            pygame.draw.rect(screen, colour, (*pos, *shape))

            # Write down fluid per cell for bug testing
            if show_fluid_count and cell.fluid != 0 and cell.dynamic:
                label = self.font.render("%.2f" % cell.fluid, 1, (0, 0, 0))
                screen.blit(label, (x * self.cell_size, y * self.cell_size))

        for x, y in np.ndindex(self.grid_size, self.grid_size):
            cell = self.grid[x, y]

            # Skip over solid cells, empty cells
            if not cell.dynamic or cell.fluid == 0:
                continue

            # Get adjacent cells
            cell_down = None if y + 1 >= self.grid_size else self.grid[x, y + 1]
            cell_left = None if x - 1 < 0 else self.grid[x - 1, y]
            cell_right = None if x + 1 >= self.grid_size else self.grid[x + 1, y]
            cell_up = None if y - 1 < 0 else self.grid[x, y - 1]

            # Flow downwards
            if cell_down is not None and cell_down.dynamic:
                flow = calculate_vertical_flow(cell.fluid, cell_down) - cell_down.fluid

                flow = np.amin((np.amax((flow, 0)), max_flow))
                flow = np.amin((cell.fluid, flow))

                cell.d_fluid -= flow
                cell_down.d_fluid += flow

                if flow != 0:
                    cell_down.falling = True

            # Check cell isn't empty
            if cell.fluid + cell.d_fluid < min_value:
                continue

            # Flow left
            if cell_left is not None and cell_left.dynamic:
                flow = (cell.fluid + cell.d_fluid - cell_left.fluid) / 4.0

                flow = np.amin((np.amax((flow, 0)), max_flow))

                cell.d_fluid -= flow
                cell_left.d_fluid += flow

            # Check cell isn't empty
            if cell.fluid + cell.d_fluid < min_value:
                continue

            # Flow right
            if cell_right is not None and cell_right.dynamic:
                flow = (cell.fluid + cell.d_fluid - cell_right.fluid) / 4.0

                flow = np.amin((np.amax((flow, 0)), max_flow))

                cell.d_fluid -= flow
                cell_right.d_fluid += flow

            # Check cell isn't empty
            if cell.fluid + cell.d_fluid < min_value:
                continue

            # Flow up
            if cell_up is not None and cell_up.dynamic:
                flow = (cell.fluid + cell.d_fluid) - calculate_vertical_flow(cell.fluid + cell.d_fluid, cell_up)

                flow = np.amin((np.amax((flow, 0)), max_flow))

                cell.d_fluid -= flow
                cell_up.d_fluid += flow

    def update(self):
        # Put everything in the render loop to improve performance
        return

    def input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            x = int(x_mouse / self.cell_size)
            y = int(y_mouse / self.cell_size)
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                self.adding_block = not self.grid[x, y].dynamic

        if pygame.mouse.get_pressed()[0]:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            x = int(x_mouse / self.cell_size)
            y = int(y_mouse / self.cell_size)
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                self.grid[x, y].fluid = 0
                self.grid[x, y].dynamic = self.adding_block

        if pygame.mouse.get_pressed()[2]:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            x = int(x_mouse / self.cell_size)
            y = int(y_mouse / self.cell_size)
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                if self.grid[x, y].dynamic:
                    self.grid[x, y].fluid += 1

    def reset(self):
        return
