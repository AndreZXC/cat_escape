import pygame
import os
import sys


pygame.init()
size = width, height = 720, 720
screen = pygame.display.set_mode(size)
tile_width = tile_height = 36


def load_image(name):
    fullname = os.path.join('textures', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


background_image = pygame.transform.smoothscale(load_image('background.png'), (width, height))


class Grass(pygame.sprite.Sprite):
    grass_images = {(True, True, True, False): load_image('grass_block\\bottom_cutted.png'),
                    (True, True, False, True): load_image('grass_block\\top_cutted.png'),
                    (True, False, True, True): load_image('grass_block\\right_cutted.png'),
                    (False, True, True, True): load_image('grass_block\\left_cutted.png'),
                    (True, True, True, True): load_image('grass_block\\not_cutted.png'),
                    (True, False, False, True): load_image('grass_block\\top_right_cutted.png'),
                    (False, True, False, True): load_image('grass_block\\top_left_cutted.png'),
                    (True, False, True, False): load_image('grass_block\\bottom_right_cutted.png'),
                    (False, True, True, False): load_image('grass_block\\bottom_left_cutted.png'),
                    (False, False, True, True): load_image('grass_block\\right_left_cutted.png'),
                    (True, True, False, False): load_image('grass_block\\top_bottom_cutted.png'),
                    (False, False, False, True): load_image('grass_block\\bottom_ledge.png'),
                    (False, False, True, False): load_image('grass_block\\top_ledge.png'),
                    (True, False, False, False): load_image('grass_block\\right_ledge.png'),
                    (False, True, False, False): load_image('grass_block\\left_ledge.png'),
                    (False, False, False, False): load_image('grass_block\\all_cutted.png')
                    }
    for k in grass_images.keys():
        grass_images[k] = pygame.transform.smoothscale(grass_images[k], (tile_width, tile_height))

    def __init__(self, x, y, mode):
        super().__init__(grass)
        self.image = Grass.grass_images[mode]
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


class Door(pygame.sprite.Sprite):
    door_image = pygame.transform.smoothscale(load_image('door.png'), (tile_width, tile_height))

    def __init__(self, x, y):
        super().__init__(door_gr)
        self.image = Door.door_image
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


def load_level(level):
    fullname = os.path.join('levels', level)
    if not os.path.isfile(fullname):
        print(f"Файл уровня '{fullname}' не найден")
        sys.exit()
    with open(fullname, 'r') as lvl:
        level_map = [line.strip() for line in lvl]
        level = list(map(lambda x: x.ljust(width // tile_width, 'g'), level_map))
        for i in range(height // tile_height - len(level)):
            level.append('g' * (width // tile_width))
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == 'g':
                    h1 = h2 = v1 = v2 = False
                    if x == 0:
                        h1 = True
                    elif level[y][x - 1] == 'g':
                        h1 = True
                    if x == len(level[y]) - 1:
                        h2 = True
                    elif level[y][x + 1] == 'g':
                        h2 = True
                    if y == 0:
                        v1 = True
                    elif level[y - 1][x] == 'g':
                        v1 = True
                    if y == len(level) - 1:
                        v2 = True
                    elif level[y + 1][x] == 'g':
                        v2 = True
                    Grass(x, y, (h1, h2, v1, v2))
                if level[y][x] == 'd':
                    Door(x, y)


grass = pygame.sprite.Group()
door_gr = pygame.sprite.Group()
load_level('1.txt')
plaing = True
while plaing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            plaing = False
    pygame.display.flip()
    screen.blit(background_image, (0, 0))
    grass.draw(screen)
    door_gr.draw(screen)