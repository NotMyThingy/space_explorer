import pygame

# import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys) -> None:
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(2, 0)


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # ESC key pressed
            if event.key == K_ESCAPE:
                running = False

        # if 'close window' was clicked
        elif event.type == QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()

    # update player
    player.update(keys_pressed)

    screen.fill((0, 0, 0))

    screen.blit(player.surf, player.rect)

    pygame.display.flip()
