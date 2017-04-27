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

class Enterprise(pygame.sprite.Sprite):
    def __init__(self):
        super(). __init__()
        self.image, self.rect = load_image("ship_enterprise.png", WHITE)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos


class TheGame:
    DISPLAY_SIZE = (1200, 700)

    def __init__(self):
        self.screen = None
        self.bg_image = None

        pygame.init()

    def init_display(self, display_width, display_height):
        mode = pygame.RESIZABLE
        size = (display_width, display_height)
        self.screen = pygame.display.set_mode(size, mode)

        self.bg_image, _ = load_image('background2.jpg')

        # Apply the background
        self.screen.blit(self.bg_image, (0, 0))

    def run(self):
        # initial display setup
        self.init_display(*self.DISPLAY_SIZE)
        pygame.display.set_caption('STAR TREK WARS I')
        pygame.display.update()

        self.handle_events()

        pygame.quit()

    def handle_events(self):
        full_screen_update = False

        clock = pygame.time.Clock()

        enterprise = Enterprise()
        allsprites = pygame.sprite.RenderUpdates((enterprise,))

        while True:
            # limit loop to 60 frames per second
            clock.tick(60)

            # Handle Input Events
            for event in pygame.event.get():
                if event.type == const.QUIT:
                    return
                elif event.type == const.KEYDOWN and event.key == const.K_ESCAPE:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    self.init_display(event.w, event.h)
                    full_screen_update = True

            allsprites.update()

            if full_screen_update:
                pygame.display.update()
            else:
                changes = allsprites.draw(self.screen)
                pygame.display.update(changes)


if __name__ == '__main__':
    TheGame().run()
