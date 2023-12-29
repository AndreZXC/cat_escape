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


grass_images = {'bottom': load_image('grass_block\\bottom_cutted.png'),
                'top': load_image('grass_block\\top_cutted.png'),
                'right': load_image('grass_block\\right_cutted.png'),
                'left': load_image('grass_block\\left_cutted.png'),
                'default': load_image('grass_block\\not_cutted.png'),
                'top_right': load_image('grass_block\\top_right_cutted.png'),
                'top_left': load_image('grass_block\\top_left_cutted.png'),
                'bottom_right': load_image('grass_block\\bottom_right_cutted.png'),
                'bottom_left': load_image('grass_block\\bottom_left_cutted.png'),
                'right_left': load_image('grass_block\\right_left_cutted.png'),
                'top_bottom': load_image('grass_block\\top_bottom_cutted.png'),
                'bottom_ledge': load_image('grass_block\\bottom_ledge.png'),
                'top_ledge': load_image('grass_block\\top_ledge.png'),
                'right_ledge': load_image('grass_block\\right_ledge.png'),
                'left_ledge': load_image('grass_block\\left_ledge.png'),
                'all': load_image('grass_block\\all_cutted.png')
                }


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y, mode):
        super().__init__(grass)
        self.image = grass_images[mode]
        self.image = pygame.transform.smoothscale(self.image, (tile_width, tile_height))
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


grass = pygame.sprite.Group()
for i in range(len(grass_images.keys())):
    Grass(i, i, list(grass_images.keys())[i])
plaing = True
background_image = load_image('background.png')
background_image = pygame.transform.smoothscale(background_image, (width, height))
while plaing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            plaing = False
    pygame.display.flip()
    screen.blit(background_image, (0, 0))
    grass.draw(screen)