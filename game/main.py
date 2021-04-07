import pygame
import player, enemy, platform, bullet, things, cam, tools, pyganim
import os

FILE_DIR = os.path.dirname(__file__)

WIDTH = 800
HEIGHT = 640

BLOCK_WIDTH = 32
BLOCK_HEIGHT = 32

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()

def main():
    while True:
        pygame.init()
        screen = pygame.display.set_mode((500, 500))
        clock = pygame.time.Clock()
        background_image = pygame.image.load('plim/fon.jpg')
        num = 1
        go = True
        game = False
        start = False

        while go:
            clock.tick(60)
            screen.blit(background_image, (0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game = True
                    go = False

        while game:
            screen = pygame.display.set_mode((800, 640))
            bg = pygame.image.load('plim/bg.png')
            pygame.display.set_caption('---')
            tools.loadLevel(num)

            left = False
            right = False
            jump = False
            fire = False

            x=y=0

            blocks = []
            enemy_coords = []
            things_coords = []
            p_coords = []
            power_coords = []
            b_coords = []
            d_coords = []

            obj = pygame.sprite.Group()

            for row in tools.level:
                for sym in row:
                    if sym == '-':
                        b = platform.Platform(x, y)
                        obj.add(b)
                        blocks.append(b)
                    if sym == '.':
                        d = platform.Block(x, y)
                        obj.add(d)
                        blocks.append(d)
                    if sym == ',':
                        bs = platform.Block_with_spikes(x, y)
                        obj.add(bs)
                        blocks.append(bs)
                    if sym == 'l':
                        lava = platform.Lava(x, y)
                        obj.add(lava)
                        blocks.append(lava)
                    if sym == '!':
                        en = enemy.Default_enemy(x, y)
                        obj.add(en)
                        enemy.enemies.add(en) 
                    if sym == 't':
                        tng = things.Hp(x, y)
                        obj.add(tng)
                        things.hp.add(tng)
                    if sym == 'P':
                        p_coords = [x, y]
                    if sym == 'p':
                        power_coords = [x, y]
                    if sym == 'b':
                        boss_en = enemy.Boss_enemy(x, y - 2)
                        obj.add(boss_en)
                        enemy.enemies.add(boss_en)
                    if sym == 'd':
                        d_coords = [x, y]

                    x += BLOCK_WIDTH

                y += BLOCK_HEIGHT
                x = 0

            power = things.Power(power_coords[0], power_coords[1])
            obj.add(power)

            playerr = player.Player(p_coords[0], p_coords[1])
            obj.add(playerr)

            door = things.Door(d_coords[0], d_coords[1])
            obj.add(door)

            total_level_width = len(tools.level[0]) * BLOCK_WIDTH
            total_level_height = len(tools.level) * BLOCK_HEIGHT 
            camera = cam.Camera(cam.start_camera, total_level_width, total_level_height)

            start = True

            while start:

                clock.tick(60)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise SystemExit
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                        left = True
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        right = True
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        jump = True
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        fire = True
                        playerr.shoot()
                    # if event.type == pygame.KEYDOWN and event.key == pygame.K_SHIFT:
                    #     playerr.grenade()
                    if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                        left = False
                    if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                        right = False
                    if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                        jump = False
                    if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                        fire = False

                screen.blit(bg, (0, 0))

                camera.update(playerr)
                playerr.update(left, right, jump, fire, blocks)
                playerr.draw_shield_bar(screen, 40, 40)
                enemy.enemies.update(playerr, player.player_bl, blocks)
                enemy.enemy_bl.update(blocks)
                player.player_bl.update(power, blocks)
                # playerr.player_grnd.update()
                things.hp.update(player.player_bl, playerr)
                power.update(player.player_bl, playerr)

                for e_bullet in enemy.enemy_bl:
                    obj.add(e_bullet)

                for p_bullet in player.player_bl:
                    obj.add(p_bullet)

                for o in obj:
                    screen.blit(o.image, camera.show(o))

                if playerr.is_dead():
                    start = False
                    game = False
                    go = True

                if pygame.sprite.collide_rect(playerr, door):
                    start = False
                    num += 1
                    for o in obj:
                        o.kill()


                pygame.display.update()

if __name__ == '__main__':
    main()





















