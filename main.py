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
        self.image = pygame.image.load("images/spaceship.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(100, SCREEN_HEIGHT / 2)
        )

    def update(self, pressed_keys) -> None:
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -2)
            move_up_sound.play()
        if pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, 2)
            move_down_sound.play()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(2, 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('images/missile.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
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
        self.image = pygame.image.load(f'images/planet_{randint(1, 17):0>2}.png').convert_alpha()
        scale = randint(80, 160)
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.image.set_colorkey((0, 0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(
                randint(SCREEN_WIDTH + 80, SCREEN_WIDTH + 150),
                randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self) -> None:
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()


pygame.mixer.init()
pygame.init()

# had to setup a clock for decent framerate as everything was moving on supersonic speed!!!
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load background and set initial positions for both instances - two images looping
bg = pygame.image.load('images/bg.png').convert()
bg_x1 = 0
bg_x2 = bg.get_width()

# a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)
ADDPLANET = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPLANET, 10000)

player = Player()
enemies = pygame.sprite.Group()
planets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# load and play some mood music to get in the zone...
# Sound source: Chris Bailey - artist Tripnet
# License: https://creativecommons.org/licences/by/3.0/
pygame.mixer.music.load('sound/Sky_dodge_theme.ogg')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

# sound effects
move_up_sound = pygame.mixer.Sound('sound/Jet_up.ogg')
move_down_sound = pygame.mixer.Sound('sound/Jet_down.ogg')
collision_sound = pygame.mixer.Sound('sound/Boom.ogg')

move_up_sound.set_volume(0.8)
move_down_sound.set_volume(0.8)
collision_sound.set_volume(1.0)

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

    # update enemies and planets
    enemies.update()
    planets.update()

    bg_x1 -= 0.5
    bg_x2 -= 0.5

    if bg_x1 < bg.get_width() * -5:
        bg_x1 = bg.get_width()
    if bg_x2 < bg.get_width() * -1:
        bg_x2 = bg.get_width()

    screen.blit(bg, (bg_x1, 0))
    screen.blit(bg, (bg_x2, 0))

    # draw all the entities
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # check for collision
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

        move_up_sound.stop()
        move_down_sound.stop()
        pygame.mixer.music.stop()
        pygame.time.delay(50)
        collision_sound.play()
        pygame.time.delay(1000)

        running = False

    pygame.display.flip()

    clock.tick(30)

pygame.mixer.quit()
