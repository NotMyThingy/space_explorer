import pygame
from random import randint

# import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/spaceship.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(100, SCREEN_HEIGHT / 2)
        )

    def update(self, pressed_keys) -> None:
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(2, 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('images/missile.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = randint(2, 5)

    def update(self) -> None:
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super(Planet, self).__init__()
        self.surf = pygame.image.load(f'images/planet0{randint(3, 5)}.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self) -> None:
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()


pygame.init()

# had to setup a clock for decent framerate as everything was moving on supersonic speed!!!
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDPLANET = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPLANET, 3000)

player = Player()
enemies = pygame.sprite.Group()
planets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

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

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDPLANET:
            new_planet = Planet()
            planets.add(new_planet)
            all_sprites.add(new_planet)

    # get the set of keys pressed, check for user input and update
    keys_pressed = pygame.key.get_pressed()
    player.update(keys_pressed)

    # updates enemies and planets
    enemies.update()
    planets.update()

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    pygame.display.flip()

    clock.tick(60)
