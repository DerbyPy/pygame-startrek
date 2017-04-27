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


class Torpedo(pygame.sprite.Sprite):
    def __init__(self):
        super(). __init__()
        self.image, self.rect = load_image("federation_torpedo.png", BLACK)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed


class Warbird(pygame.sprite.Sprite):
    def __init__(self):
        super(). __init__()
        self.image, self.rect = load_image("ship_warbird.png", WHITE)

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.right = self.area.right
        self.rect.top = 10
        self.move_y = 4

    def update(self):
        newpos = self.rect.move((0, self.move_y))
        if newpos.bottom > self.area.bottom or \
                newpos.top < self.area.top:
            self.move_y = -self.move_y
            newpos = self.rect.move((0, self.move_y))
        self.rect = newpos


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
        clock = pygame.time.Clock()
        enterprise = Enterprise()
        warbird = Warbird()
        allsprites = pygame.sprite.RenderUpdates((enterprise, warbird))
        torpedo_list = pygame.sprite.Group()

        while True:
            full_screen_update = False

            # limit loop to 60 frames per second
            clock.tick(60)

            # clear previous draws to avoid trailing effect
            allsprites.clear(self.screen, self.bg_image)

            # Handle Input Events
            for event in pygame.event.get():
                if event.type == const.QUIT:
                    return
                elif event.type == const.KEYDOWN and event.key == const.K_ESCAPE:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    self.init_display(event.w, event.h)
                    full_screen_update = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    torpedo = Torpedo()
                    # Set the torpedo so it is where the player is
                    torpedo.rect.center = enterprise.rect.center
                    # Add the torpedo to the lists
                    allsprites.add(torpedo)
                    torpedo_list.add(torpedo)

            allsprites.update()

            # Collision mechanics for torpedos & warbird
            for torpedo in pygame.sprite.spritecollide(warbird, torpedo_list, True):
                torpedo_list.remove(torpedo)
                allsprites.remove(torpedo)

            if full_screen_update:
                pygame.display.update()
            else:
                changes = allsprites.draw(self.screen)
                pygame.display.update(changes)


if __name__ == '__main__':
    TheGame().run()
