import random
import pygame
pygame.init()
# **************************************************************
# FileName: plane_sprites.py***************************************
# Author:  Junieson *********************************************
# Version:  2019.8.12 ******************************************
# ****************************************************************
# 分数
SCORE = 0
# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# color
color_blue = (30, 144, 255)
color_green = (0, 255, 0)
color_red = (255, 0, 0)
color_purple = (148, 0, 211)
color_gray = (251, 255, 242)
# 刷新的帧率
FRAME_PER_SEC = 60  # 刷新率是60hz,即每秒update60次
# 创建敌机的定时器常量,自定义用户事件,其实就是int数,不同数表示不同事件
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1
# buff1 出现的事件
BUFF1_SHOW_UP = pygame.USEREVENT + 2
# buff2
BUFF2_SHOW_UP = pygame.USEREVENT + 3
# 敌军发射子弹
ENEMY_FIRE_EVENT = pygame.USEREVENT + 4
# 发射炸弹
BOMB_THROW = pygame.USEREVENT + 5


class GameScore(object):
    global SCORE

    def __init__(self):
        self.score = 0
        pass

    def getvalue(self):
        self.score = SCORE
        return self.score


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speedy=1, speedx=0):
        # 调用父类的初始化方法
        super().__init__()

        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speedy = speedy
        self.speedx = speedx
        self.injury = 1
        self.index = 0  # 记帧数变量
        self.bar = bloodline(color_blue, self.rect.x, self.rect.y - 10, self.rect.width)

    def update(self):
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        self.bar.x = self.rect.x
        self.bar.y = self.rect.y - 10


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):

        # 1. 调用父类方法实现精灵的创建(image/rect/speed)
        super().__init__("./images/background.png")

        # 2. 判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        # 1. 调用父类的方法实现
        super().update()

        # 2. 判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Boss(GameSprite):

    def __init__(self):
        super().__init__("./images/enemy3_n1.png", 0, 1)
        self.music_boom = pygame.mixer.Sound("./music/enemy3_down.wav")
        self.music_fly = pygame.mixer.Sound("./music/enemy3_flying.wav")
        self.music_fly.play(-1)
        self.rect.centerx = 240
        self.y = 200
        self.isboom = False
        self.number = 3
        self.index1 = 1  # 控制动画速度
        self.index2 = 0
        self.index3 = 0
        self.index4 = 0
        self.injury = 1
        self.bar = bloodline(color_purple, 0, 0, 480, 8, 200)
        self.bullets = pygame.sprite.Group()

    def fire(self):
            for j in range(2, 7):  # 每层5个
                bullet = Bullet(0, 1)
                bullet.injury = 1
                # 2. 设置精灵的位置
                bullet.rect.centerx = self.rect.centerx
                bullet.rect.y = self.rect.bottom
                if j == 2:
                    bullet.speedx = 0
                else:
                    bullet.speedx = (-1) ** j * ((j - 1) // 2) * 1

                self.bullets.add(bullet)

    def update(self):
        # 左右移
        global SCORE
        if self.index4 % 2 == 0:  # 降低帧速率,注意这两个指针不能一样
            # 内部为左右移动大概50像素
            if self.index3 % 50 == 0 and (self.index3 // 50) % 2 == 1:
                self.speedx = -self.speedx
            self.rect.x += self.speedx
            self.index3 += 1
        self.index4 += 1

        # 发电动画
        self.image = pygame.image.load("./images/enemy3_n" + str((self.index1 // 6) % 2 + 1) + ".png")
        self.index1 += 1

        # 爆炸动画
        if self.isboom:
            self.bar.length -= self.injury * self.bar.weight
            if self.bar.length <= 0:  # 此时满足爆炸的条件了
                self.music_fly.stop()
                if self.index2 == 0:
                    self.music_boom.play()
                if self.index2 < 29:  # 4*7+1
                    self.image = pygame.image.load("./images/enemy3_down" + str(self.index2 // 7) + ".png")
                    # 这个地方之所以要整除4是为了减慢爆炸的速度，如果按照update的频率60hz就太快了
                    self.index2 += 1
                else:
                    self.kill()
                    SCORE += self.bar.value
            else:
                self.isboom = False  # 否则还不能死


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self, num=1):
        self.number = num
        # 1. 调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__("./images/enemy" + str(num) + ".png")

        # music
        if num == 1:
            self.music_boom = pygame.mixer.Sound("./music/enemy1_down.wav")
        else:
            self.music_boom = pygame.mixer.Sound("./music/enemy2_down.wav")
        # 2. 指定敌机的初始随机速度 1 ~ 3
        self.speedy = random.randint(1, 3)

        # 3. 指定敌机的初始随机位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

        # 4.爆炸效果
        self.isboom = False
        self.index = 0

        # 5.血条
        if self.number == 1:
            self.bar = bloodline(color_blue, self.rect.x, self.rect.y, self.rect.width)
        else:
            self.bar = bloodline(color_blue, self.rect.x, self.rect.y, self.rect.width, 3, 4)

        # 6,子弹
        self.bullets = pygame.sprite.Group()

    def fire(self):
        for i in range(0, 2):
            # 1. 创建子弹精灵
            bullet = Bullet(0, random.randint(self.speedy + 1, self.speedy + 3))
            # 2. 设置精灵的位置
            bullet.rect.bottom = self.rect.bottom + i * 20
            bullet.rect.centerx = self.rect.centerx

            # 3. 将精灵添加到精灵组
            self.bullets.add(bullet)

    def update(self):
        global SCORE
        # 1. 调用父类方法，保持垂直方向的飞行
        super().update()

        # 2. 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y > SCREEN_RECT.height:
            # print("飞出屏幕，需要从精灵组删除...")
            # kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()
            self.bar.length = 0

        if self.isboom:
            self.bar.length -= self.bar.weight * self.injury
            if self.bar.length <= 0:
                if self.index == 0:  # 保证只响一次
                    self.music_boom.play()
                if self.index < 17:  # 4*4+1
                    self.image = pygame.image.load(
                        "./images/enemy" + str(self.number) + "_down" + str(self.index // 4) + ".png")
                    # 这个地方之所以要整除4是为了减慢爆炸的速度，如果按照update的频率60hz就太快了
                    self.index += 1
                else:
                    self.kill()
                    SCORE += self.bar.value


            else:
                self.isboom = False


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):
        # 1. 调用父类方法，设置image&speed
        super().__init__("./images/me1.png")
        self.music_down = pygame.mixer.Sound("./music/me_down.wav")
        self.music_upgrade = pygame.mixer.Sound("./music/upgrade.wav")
        self.music_degrade = pygame.mixer.Sound("./music/supply.wav")

        self.number = 0
        # 2. 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 3. 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()
        # 4.爆炸
        self.isboom = False
        self.index1 = 1  # 控制动画速度
        self.index2 = 0
        # 5.buff1加成
        self.buff1_num = 0
        # 6,英雄血条
        self.bar = bloodline(color_green, 0, 700, 480, 8, 10)
        # 7，炸弹数目
        self.bomb = 0

    def update(self):

        # 英雄在水平方向移动和血条不同步,特殊
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # 控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

        # 英雄喷气动画

        self.image = pygame.image.load("./images/me" + str((self.index1 // 6) % 2 + 1) + ".png")
        self.index1 += 1

        # 英雄爆炸动画
        if self.isboom:
            self.bar.length -= self.injury * self.bar.weight
            if self.bar.length <= 0:  # 此时满足爆炸的条件了
                if self.index2 == 0:
                    self.music_down.play()
                if self.index2 < 17:  # 4*4+1
                    self.image = pygame.image.load("./images/me_destroy_" + str(self.index2 // 4) + ".png")
                    # 这个地方之所以要整除4是为了减慢爆炸的速度，如果按照update的频率60hz就太快了
                    self.index2 += 1
                else:
                    self.kill()
            else:
                self.isboom = False  # 否则还不能死

    # 发射子弹
    def fire(self):
        if self.buff1_num == 0:
            for i in range(0, 1):
                # 1. 创建子弹精灵
                bullet = Bullet()

                # 2. 设置精灵的位置
                bullet.rect.bottom = self.rect.y - i * 20
                bullet.rect.centerx = self.rect.centerx

                # 3. 将精灵添加到精灵组
                self.bullets.add(bullet)
        elif self.buff1_num <= 3:
            for i in (0, 1):
                # 1. 创建子弹精灵
                for j in range(2, self.buff1_num + 3):
                    bullet = Bullet(2, -3)
                    # 2. 设置精灵的位置
                    bullet.rect.bottom = self.rect.y - i * 20
                    if (self.buff1_num % 2 == 1):
                        bullet.rect.centerx = self.rect.centerx + (-1) ** j * 15 * (j // 2)
                    if (self.buff1_num % 2 == 0):
                        if j == 2:
                            bullet.rect.centerx = self.rect.centerx
                        else:
                            bullet.rect.centerx = self.rect.centerx + (-1) ** j * 15 * ((j - 1) // 2)
                    # 3. 将精灵添加到精灵组
                    self.bullets.add(bullet)
        elif self.buff1_num >= 4:
            for i in range(0, 1):
                # 1. 表示有几层
                for j in range(2, 5):  # 每层三个

                    bullet = Bullet(3, -3)
                    bullet.injury = 2
                    # 2. 设置精灵的位置
                    bullet.rect.bottom = self.rect.y
                    if j == 2:
                        bullet.rect.centerx = self.rect.centerx
                    else:
                        bullet.rect.centerx = self.rect.centerx + (-1) ** j * (30 + 5 * i)
                        bullet.speedx = (-1) ** j * (i + 1)
                    self.bullets.add(bullet)


class Heromate(Hero):
    def __init__(self, num):
        super().__init__()
        self.image = pygame.image.load("./images/life.png")
        self.number = num

    def update(self):

        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

    def fire(self):
        for i in range(0, 1, 2):
            # 1. 创建子弹精灵
            bullet = Bullet()
            # 2. 设置精灵的位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # 3. 将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self, color=1, speedy=-2, speedx=0):
        # 调用父类方法，设置子弹图片，设置初始速度
        self.hity = color  # 子弹伤害值
        self.music_shoot = pygame.mixer.Sound("./music/bullet.wav")
        self.music_shoot.set_volume(0.4)
        if color > 0:  # 只让英雄发子弹响
            self.music_shoot.play()
        super().__init__("./images/bullet" + str(color) + ".png", speedy, speedx)

    def update(self):
        # 调用父类方法，让子弹沿垂直方向飞行
        super().update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0 or self.rect.y > 700:
            self.kill()


class Buff1(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet_supply.png", 1)
        self.music_get = pygame.mixer.Sound("./music/get_bullet.wav")
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()


class Buff2(GameSprite):
    def __init__(self):
        super().__init__("./images/bomb_supply.png", 2)
        self.music_get = pygame.mixer.Sound("./music/get_bomb.wav")
        self.rect.bottom = random.randint(0, 700)
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        self.ran = random.randint(60, 180)  # 在持续1~3s后消失

    def update(self):
        super().update()
        if self.rect.bottom < 0 or self.index == self.ran:
            self.kill()
        self.index += 1

class Buff3(Buff2):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/buff3.png")
        self.speedy=3


class bloodline(object):
    def __init__(self, color, x, y, length, width=2, value=2):
        self.color = color
        self.x = x
        self.y = y
        self.length = length
        self.width = width  # 线宽
        self.value = value * 1.0  # 血量用浮点数
        self.weight = length / value  # 每一滴血表示的距离
        self.color_init = color

    def update(self, canvas):
        if self.length <= self.value * self.weight / 2:
            self.color = color_red
        else:
            self.color = self.color_init
        self.bar_rect = pygame.draw.line(canvas, self.color, (self.x, self.y), (self.x + self.length, self.y),
                                         self.width)


class CanvasOver():
    def __init__(self, screen):
        self.img_again = pygame.image.load("./images/again.png")
        self.img_over = pygame.image.load("./images/gameover.png")
        self.rect_again = self.img_again.get_rect()
        self.rect_over = self.img_over.get_rect()
        self.rect_again.centerx = self.rect_over.centerx = SCREEN_RECT.centerx
        self.rect_again.bottom = SCREEN_RECT.centery
        self.rect_over.y = self.rect_again.bottom + 20
        self.screen = screen

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect_again.left < pos[0] < self.rect_again.right and \
                    self.rect_again.top < pos[1] < self.rect_again.bottom:
                return 1
            elif self.rect_over.left < pos[0] < self.rect_over.right and \
                    self.rect_over.top < pos[1] < self.rect_over.bottom:
                return 0

    def update(self):
        self.screen.blit(self.img_again, self.rect_again)
        self.screen.blit(self.img_over, self.rect_over)
        score_font = pygame.font.Font("./STCAIYUN.ttf", 50)
        image = score_font.render("SCORE:" + str(int(SCORE)), True, color_gray)
        rect = image.get_rect()
        rect.centerx, rect.bottom = SCREEN_RECT.centerx, self.rect_again.top - 20
        self.screen.blit(image, rect)
