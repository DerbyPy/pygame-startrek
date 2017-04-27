import os

import pygame
import pygame.constants as const
from pygame.compat import geterror


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, const.RLEACCEL)
    return image, image.get_rect()


class TheGame:
    DISPLAY_SIZE = (700, 500)

    def __init__(self):
        self.screen = None
        self.bg_image = None

        pygame.init()

        # Initialize the screen
        self.screen = pygame.display.set_mode(self.DISPLAY_SIZE)
        self.bg_image, _ = load_image('background.jpg')
        self.screen.blit(self.bg_image, (0, 0))

    def run(self):
        pygame.display.set_caption('STAR TREK WARS I')
        pygame.display.update()

        self.handle_events()

        pygame.quit()

    def handle_events(self):
        clock = pygame.time.Clock()

        while True:
            # limit loop to 60 frames per second
            clock.tick(60)

            # Handle Input Events
            for event in pygame.event.get():
                if event.type == const.QUIT:
                    return
                elif event.type == const.KEYDOWN and event.key == const.K_ESCAPE:
                    return

            pygame.display.update()


if __name__ == '__main__':
    TheGame().run()
