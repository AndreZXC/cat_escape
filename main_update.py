import pygame
import os
import sys

pygame.init()
size = width, height = 720, 720
screen = pygame.display.set_mode(size)
tile_width = tile_height = 36
all_sprites = pygame.sprite.Group()
grass = pygame.sprite.Group()
door_gr = pygame.sprite.Group()
money_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
buttons = pygame.sprite.Group()
spikes_gr = pygame.sprite.Group()
lvl = 0
fps = 60
clock = pygame.time.Clock()


def load_image(name):
    fullname = os.path.join('textures', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


background_image = pygame.transform.smoothscale(load_image('background.png'), (width, height))
title_image = pygame.transform.smoothscale(load_image('glav.png'), (630, 310))
pygame.display.set_icon(load_image('cat\\cat_base.png'))
pygame.display.set_caption('Котик в бегах — by Andre and Eleonora')


def load_level(level):
    fullname = os.path.join('levels', level)
    if not os.path.isfile(fullname):
        print(f"Файл уровня '{fullname}' не найден")
        sys.exit()
    with open(fullname, 'r') as file:
        level_map = [line.strip() for line in file]
        level = list(map(lambda x: x.ljust(width // tile_width, 'g'), level_map))
        for i in range(height // tile_height - len(level)):
            level.append('g' * (width // tile_width))
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] in ('g', 's'):
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
                    if level[y][x] == 'g':
                        Grass(x, y, (h1, h2, v1, v2))
                    else:
                        Spike(x, y, (h1, h2, v1, v2))
                if level[y][x] == 'd':
                    Door(x, y)
                if level[y][x] == 'm':
                    Money(x, y)
                if level[y][x] == 'c':
                    player = Player(x, y)
        return player


class Start(pygame.sprite.Sprite):
    image = pygame.transform.smoothscale(load_image('buttons\\start.png'), (270, 81))
    image_2 = pygame.transform.smoothscale(load_image('buttons\\start_2.png'), (270, 81))

    def __init__(self):
        super().__init__(buttons, all_sprites)
        self.image = Start.image
        self.rect = self.image.get_rect().move(width // 2 - self.image.get_width() // 2,
                                               height // 3 * 2 - self.image.get_height() // 2)

    def update(self, pos, change_mode):
        if change_mode == 'move':
            if self.rect.collidepoint(pos):
                self.image = Start.image_2
            else:
                self.image = Start.image
        if change_mode == 'press':
            if self.rect.collidepoint(pos):
                global all_sprites, buttons
                all_sprites.empty()
                buttons.empty()


class LevelBtn(pygame.sprite.Sprite):
    level_im = []
    level_im_2 = []
    for i in range(1, 11):
        level_im.append(pygame.transform.smoothscale(load_image(f"buttons\\level_{i}.png"),
                                                     (81, 81)))
        level_im_2.append(pygame.transform.smoothscale(load_image(f"buttons\\level_{i}_2.png"),
                                                       (81, 81)))

    def __init__(self, n):
        super().__init__(buttons, all_sprites)
        self.image = LevelBtn.level_im[n]
        self.number = n
        if 0 <= n <= 2:
            self.rect = self.image.get_rect().move((width // 4 * ((n % 3) + 1) -
                                                    self.image.get_width() // 2),
                                                   height // 5 - self.image.get_width())
        elif 3 <= n <= 5:
            self.rect = self.image.get_rect().move((width // 4 * ((n % 3) + 1) -
                                                    self.image.get_width() // 2),
                                                   height // 5 * 2 - self.image.get_width())
        elif 6 <= n <= 8:
            self.rect = self.image.get_rect().move((width // 4 * ((n % 3) + 1) -
                                                    self.image.get_width() // 2),
                                                   height // 5 * 3 - self.image.get_width())
        else:
            self.rect = self.image.get_rect().move((width // 2 - self.image.get_width() // 2),
                                                   height // 5 * 4 - self.image.get_width())

    def update(self, pos, change_mode):
        if change_mode == 'move':
            if self.rect.collidepoint(pos):
                self.image = LevelBtn.level_im_2[self.number]
            else:
                self.image = LevelBtn.level_im[self.number]
        if change_mode == 'press':
            if self.rect.collidepoint(pos):
                global buttons, all_sprites, lvl
                buttons.empty()
                all_sprites.empty()
                lvl = self.number + 1


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
                    (False, False, True, False): load_image('grass_block\\bottom_ledge.png'),
                    (False, False, False, True): load_image('grass_block\\top_ledge.png'),
                    (True, False, False, False): load_image('grass_block\\right_ledge.png'),
                    (False, True, False, False): load_image('grass_block\\left_ledge.png'),
                    (False, False, False, False): load_image('grass_block\\all_cutted.png')
                    }
    for k in grass_images.keys():
        grass_images[k] = pygame.transform.smoothscale(grass_images[k], (tile_width, tile_height))

    def __init__(self, x, y, mode):
        super().__init__(grass, all_sprites)
        self.image = Grass.grass_images[mode]
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


class Door(pygame.sprite.Sprite):
    door_image = pygame.transform.smoothscale(load_image('door.png'), (tile_width, tile_height))

    def __init__(self, x, y):
        super().__init__(door_gr, all_sprites)
        self.image = Door.door_image
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


class Money(pygame.sprite.Sprite):
    image = load_image('money.png')

    def __init__(self, x, y):
        super().__init__(money_sprites, all_sprites)
        self.frames = []
        self.cut_sheet(Money.image, 1, 12)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            frame_location = (0, self.rect.h * i)
            self.frames.append(pygame.transform.smoothscale(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)), (tile_width, tile_height)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Player(pygame.sprite.Sprite):
    images = [pygame.transform.smoothscale(load_image('cat\\cat_base.png'),
                                           (tile_width, tile_height)),
              pygame.transform.smoothscale(load_image('cat\\cat_base_1.png'),
                                           (tile_width, tile_height)),
              pygame.transform.smoothscale(load_image('cat\\cat_base_2.png'),
                                           (tile_width, tile_height)),
              pygame.transform.smoothscale(load_image('cat\\cat_base_3.png'),
                                           (tile_width, tile_height))]
    motion_img = [pygame.transform.smoothscale(load_image('cat\\cat_motion_1.png'),
                                               (tile_width, tile_height)),
                  pygame.transform.smoothscale(load_image('cat\\cat_motion_2.png'),
                                               (tile_width, tile_height)),
                  pygame.transform.smoothscale(load_image('cat\\cat_motion_3.png'),
                                               (tile_width, tile_height)),
                  pygame.transform.smoothscale(load_image('cat\\cat_motion_2.png'),
                                               (tile_width, tile_height))]
    death_img = [pygame.transform.smoothscale(load_image('cat\\cat_dead.png'),
                                              (tile_width, tile_height)),
                 pygame.transform.smoothscale(load_image('cat\\cat_dead_1.png'),
                                              (tile_width, tile_height)),
                 pygame.transform.smoothscale(load_image('cat\\cat_dead_2.png'),
                                              (tile_width, tile_height)),
                 pygame.transform.smoothscale(load_image('cat\\cat_dead_3.png'),
                                              (tile_width, tile_height))]

    def __init__(self, x, y):
        super().__init__(player_group)
        self.cash = 0
        self.image = Player.images[0]
        self.cadr = 0
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)
        self.start = x, y
        self.movement = False
        self.direction = (0, 0)
        self.life = True
        self.win = False

    def update(self, time):
        self.rect = self.rect.move(self.direction[0], self.direction[1])
        self.image = Player.motion_img[time % 4]
        if self.direction[0] < 0:
            self.image = pygame.transform.rotate(self.image, 90)
            if pygame.sprite.spritecollideany(self, spikes_gr):
                spike = pygame.sprite.spritecollideany(self, spikes_gr)
                self.rect = self.rect.move((spike.rect.width, 0))
                self.death()
        if self.direction[0] > 0:
            self.image = pygame.transform.rotate(self.image, 270)
            if pygame.sprite.spritecollideany(self, spikes_gr):
                spike = pygame.sprite.spritecollideany(self, spikes_gr)
                self.rect = self.rect.move((-spike.rect.width, 0))
                self.death()
        if self.direction[1] < 0:
            self.image = pygame.transform.rotate(self.image, 0)
            if pygame.sprite.spritecollideany(self, spikes_gr):
                spike = pygame.sprite.spritecollideany(self, spikes_gr)
                self.rect = self.rect.move((0, spike.rect.height))
                self.death()
        if self.direction[1] > 0:
            self.image = pygame.transform.rotate(self.image, 180)
            if pygame.sprite.spritecollideany(self, spikes_gr):
                spike = pygame.sprite.spritecollideany(self, spikes_gr)
                self.rect = self.rect.move((0, -spike.rect.height))
                self.death()
        if pygame.sprite.spritecollideany(self, money_sprites):
            self.get_money()
        if pygame.sprite.spritecollideany(self, door_gr):
            self.exit()
        if pygame.sprite.spritecollideany(self, grass):
            self.rect = self.rect.move((-self.direction[0], -self.direction[1]))
            self.image = Player.images[0]
            self.movement = False
            self.direction = (0, 0)

    def next_cadr(self):
        if self.cadr == 1:
            self.image = Player.images[1]
            self.cadr = 2
        elif self.cadr == 2:
            self.image = Player.images[2]
            self.cadr = 3
        elif self.cadr == 3:
            self.image = Player.images[1]
            self.cadr = 4
        elif self.cadr == 4:
            self.image = Player.images[3]
            self.cadr = 5
        elif self.cadr == 5:
            self.image = Player.images[0]
            self.cadr = 0
        if self.cadr == -1:
            self.image = Player.images[0]
            self.cadr = -2
        elif self.cadr == -2:
            self.image = Player.death_img[0]
            self.cadr = -3
        elif self.cadr == -3:
            self.image = Player.death_img[1]
            self.cadr = -4
        elif self.cadr == -4:
            self.image = Player.death_img[2]
            self.cadr = -5
        elif self.cadr == -5:
            self.image = Player.death_img[3]
            self.cadr = -6

    def death(self):
        self.life = False
        self.movement = False
        self.direction = (0, 0)
        self.cadr = -1

    def get_money(self):
        money = pygame.sprite.spritecollideany(self, money_sprites)
        money_sprites.remove(money)
        all_sprites.remove(money)
        self.cash += 1

    def exit(self):
        self.win = True


class BackBtn(pygame.sprite.Sprite):
    image = pygame.transform.smoothscale(load_image('buttons\\back.png'), (tile_width, tile_height))
    image_2 = pygame.transform.smoothscale(load_image('buttons\\back_2.png'),
                                           (tile_width, tile_height))

    def __init__(self, pos):
        super().__init__(buttons, all_sprites)
        self.image = BackBtn.image
        self.rect = self.image.get_rect().move(pos)
        self.back = False

    def update(self, pos, change_mode):
        if change_mode == 'move':
            if self.rect.collidepoint(pos):
                self.image = BackBtn.image_2
            else:
                self.image = BackBtn.image
        if change_mode == 'press':
            if self.rect.collidepoint(pos):
                self.back = True


class Spike(pygame.sprite.Sprite):
    image = load_image('spikes.png')

    def __init__(self, x, y, neigbours):
        super().__init__(all_sprites, spikes_gr)
        if neigbours[0]:
            self.image = pygame.transform.rotate(Spike.image, 270)
            self.image = pygame.transform.smoothscale(self.image,
                                                      (self.image.get_width() /
                                                       self.image.get_height() * tile_width,
                                                       tile_height))
            self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)
        elif neigbours[1]:
            self.image = pygame.transform.rotate(Spike.image, 90)
            self.image = pygame.transform.smoothscale(self.image,
                                                      (self.image.get_width() /
                                                       self.image.get_height() * tile_width,
                                                       tile_height))
            self.rect = self.image.get_rect().move(tile_width * x +
                                                   tile_width - self.image.get_width(),
                                                   tile_height * y)
        elif neigbours[2]:
            self.image = pygame.transform.rotate(Spike.image, 180)
            self.image = pygame.transform.smoothscale(self.image,
                                                      (tile_width,
                                                       self.image.get_height() /
                                                       self.image.get_width() * tile_height))
            self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)
        else:
            self.image = Spike.image
            self.image = pygame.transform.smoothscale(self.image,
                                                      (tile_width,
                                                       self.image.get_height() /
                                                       self.image.get_width() * tile_height))
            self.rect = self.image.get_rect().move(tile_width * x,
                                                   tile_height * y +
                                                   tile_height - self.image.get_height())


def start():
    Start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                buttons.update(event.pos, 'move')
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons.update(event.pos, 'press')
                if not buttons:
                    level_choice()
        pygame.display.flip()
        screen.blit(background_image, (0, 0))
        screen.blit(title_image, (width // 2 - title_image.get_width() // 2, 50))
        all_sprites.draw(screen)


def level_choice():
    for i in range(10):
        LevelBtn(i)
    backbtn = BackBtn((20, height - 20 - BackBtn.image.get_height()))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                buttons.update(event.pos, 'move')
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons.update(event.pos, 'press')
                if not buttons:
                    backbtn = game(lvl)
        if backbtn.back:
            all_sprites.empty()
            buttons.empty()
            Start()
            return
        pygame.display.flip()
        screen.blit(background_image, (0, 0))
        buttons.draw(screen)


def game(level):
    player = load_level(f'{level}.txt')
    backbtn = BackBtn((20, 20))
    MONEY_UPDATE = pygame.USEREVENT + 1
    pygame.time.set_timer(MONEY_UPDATE, 80)
    PLAYER_MOVE = pygame.USEREVENT + 2
    pygame.time.set_timer(PLAYER_MOVE, 40)
    PLAYER_ANIM = pygame.USEREVENT + 3
    pygame.time.set_timer(PLAYER_ANIM, 100)
    PLAYER_BLINKING = pygame.USEREVENT + 4
    pygame.time.set_timer(PLAYER_BLINKING, 4000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MONEY_UPDATE:
                money_sprites.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not player.movement:
                    player.direction = (-tile_width, 0)
                if event.key == pygame.K_RIGHT and not player.movement:
                    player.direction = (tile_width, 0)
                if event.key == pygame.K_DOWN and not player.movement:
                    player.direction = (0, tile_height)
                if event.key == pygame.K_UP and not player.movement:
                    player.direction = (0, -tile_height)
            if event.type == pygame.MOUSEMOTION:
                buttons.update(event.pos, 'move')
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons.update(event.pos, 'press')
            if event.type == PLAYER_MOVE:
                if any(player.direction):
                    player.movement = True
                    player_group.update(pygame.time.get_ticks())
            if event.type == PLAYER_BLINKING and not player.movement and player.life:
                player.cadr = 1
            if event.type == PLAYER_ANIM and not player.movement:
                if player.life:
                    player.next_cadr()
                else:
                    player.next_cadr()
        if backbtn.back or player.win:
            all_sprites.empty()
            grass.empty()
            door_gr.empty()
            money_sprites.empty()
            player_group.empty()
            buttons.empty()
            spikes_gr.empty()
            for i in range(10):
                LevelBtn(i)
            backbtn = BackBtn((20, height - 20 - BackBtn.image.get_height()))
            return backbtn
        if player.cadr == -6:
            all_sprites.empty()
            grass.empty()
            door_gr.empty()
            money_sprites.empty()
            player_group.empty()
            buttons.empty()
            spikes_gr.empty()
            player = load_level(f'{level}.txt')
            backbtn = BackBtn((20, 20))
        pygame.display.flip()
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        clock.tick(fps)


start()