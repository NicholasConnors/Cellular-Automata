import pygame
from Conway import Conway
from Ant import Ant
from BriansBrain import Brian
from Rule90 import Rule90
from Rule110 import Rule110


class Application:
    background_colour = (255, 255, 255)

    def __init__(self, config):
        # Initialize pygame
        pygame.init()

        # Initialize self
        self.screen = pygame.display.set_mode(config.screen_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(config.name)

        # Initialize grid of cells
        self.automaton = config.automaton

        # Set rate of simulation
        self.tps_cap = config.tps_cap

        self.run()

    def run(self):
        running = True
        while running:
            self.clock.tick(self.tps_cap)

            self.screen.fill(self.background_colour)
            self.automaton.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.automaton.input(event)

            self.automaton.update()

            # Actually draw to window
            pygame.display.flip()


class Config:
    def __init__(self, screen_size, name, tps_cap, automaton):
        self.screen_size = screen_size
        self.name = name
        self.tps_cap = tps_cap
        self.automaton = automaton


def main():
    # Start application

    config = [
        Config((640, 640), "Conway's Game of Life", 64, Conway()),
        Config((640, 640), "Langston's Ant", 64, Ant()),
        Config((640, 640), "Brian's Brain", 64, Brian()),
        Config((640, 640), "Rule 90", 64, Rule90()),
        Config((640, 640), "Rule 110", 64, Rule110())
    ]

    Application(config[0])


if __name__ == "__main__":
    main()
