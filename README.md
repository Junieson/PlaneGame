# -PlaneGame
飞机大战游戏Airplane war game

python项目_飞机大战(爆炸效果,血条,音效,buff加成,boss,菜单,完整详细注释的源码)

﻿@[TOC]
# 一. 总体概览
**话不多说,先看效果图,动作是有声音的,但是放不出来**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812182648683.gif)![在这里插入图片描述](https://img-blog.csdnimg.cn/2019081218273268.gif)![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812182926386.gif)![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812182048512.gif)![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812181748343.gif)![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812182327410.gif)
看图片应该大体有个了解,然后我再具体介绍下,游戏有哪些功能和细节
## 基本功能

 1. 键盘方向键控制英雄移动
 2. 英雄自动发射子弹
 3. 敌军飞机自动生成,向下运动,发射不同速度炮弹
 4. 自动生成 补给,有子弹buff,炸弹buff,补血buff
         4.1子弹buff最多吃5个,每吃一个子弹数目或者威力提高,吃到第五个召唤"最强形态"
        4.2炸弹buff可以无限吃,当然出现几率比较小,吃到的炸弹在屏幕左下角显示,空格键引爆一颗炸弹,毁掉当前所有敌军飞机,boss损血
        4.3补血buff,一次补满英雄血条
 5. 每种敌军对应不同分数,英雄击爆后,屏幕又下角的总分增加相应的分数
 6. 子弹击中和撞击都会时敌机和英雄损血,且英雄还会debuff,就是buff效果会减弱
 7. 当英雄挂掉,游戏结束,屏幕显示分数,并且可以选择重来或者结束游戏 


## 细节部分(全部可以自定义)
 1. 英雄吃buff初期子弹威力+1,且子弹排数有序增加,均匀分步
 2. 血条低于某个值会变红,当吃补给增加后又会恢复原色
 3. 敌机出现位置随机,速度随机,发射子弹速度随机,数量排数自定义,低级敌机出场较多,中型后来逐渐增多
 4. 英雄,boss有飞行和爆炸动画,敌机有爆炸动画
 5. 撞击对不同对象效果不同,英雄撞boss,英雄死boss损血,敌机撞英雄,敌机爆,英雄损血,且损血和被子弹击中血量不同
 6. 背景和bgm循环移动,营造飞行感觉
 7. 每个动作都有专属音效,如英雄爆,敌机爆,补习,补子弹,补炸弹,扔炸弹,射击......
 8. 三组buff出现频率不同,且出现时机不同,补血在英雄血条为红色时优先出现
 9. boss移动速度慢,慢于最低速度,即1像素每帧,游戏定义为60帧/秒,即速度低于60像素/秒
 10. 飞机不能飞出屏幕外面
 11. 敌军死后子弹留着
 12. 最强形态不增加英雄所占面积
 13. 爆炸有动画效果
 14. 子弹击爆敌机后,不继续集中残骇
 15. ......(细节部分太多,首先要有个大致的思路,然后在不断调试中找到最好配置)


## 可增添需求
**(简单重复性工作可让细节更加到位,代码看明白后可以自行添加,这是个无底洞,提供个思路)**
1. 增加历史最高分,建立变量每局更新
2. 增加个人中心,记录分数变化
3. 增加敌机,boss,改变子弹发射方式
4. 添加更多buff,增添更多特效
5. 增加关卡
6. 让敌机,buff出现的时机,数量,等级,随游戏的推进而动态变化,更加人性化
7. ... 


# 二,技术框架
主要就是python类和pygame模块的运用,有项目文件后直接安装pygame库就可以运行了
## 核心技术概述
### 1.游戏的初始化和退出
* 要使用 `pygame` 提供的所有功能之前，需要调用 `init` 方法
* 在游戏结束前需要调用一下 `quit` 方法 

| 方法            | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| `pygame.init()` | 导入并初始化所有 `pygame` 模块，使用其他模块之前，必须先调用 `init` 方法 |
| `pygame.quit()` | 卸载所有 `pygame` 模块，在游戏结束之前调用！                 |
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812192727231.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2k2MjIzNjcx,size_16,color_FFFFFF,t_70)
import pygame

pygame.init()==这个模块初始化一定不能省略==

游戏代码...

pygame.quit()

### 2 理解游戏中的坐标系

* **坐标系**
    * **原点** 在 **左上角** `(0, 0)`
    * **x 轴** 水平方向向 **右**，逐渐增加
    * **y 轴** 垂直方向向 **下**，逐渐增加
* 在游戏中，**所有可见的元素** 都是以 **矩形区域** 来描述位置的![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812193035717.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2k2MjIzNjcx,size_16,color_FFFFFF,t_70)
 * 要描述一个矩形区域有四个要素：`(x, y) (width, height)`

* `pygame` 专门提供了一个类 `pygame.Rect` 用于描述 **矩形区域**

```python
Rect(x, y, width, height) -> Rect
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812193047916.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2k2MjIzNjcx,size_16,color_FFFFFF,t_70)
### 3 创建游戏主窗口

* `pygame` 专门提供了一个 **模块** `pygame.display` 用于创建、管理 **游戏窗口**

| 方法                        | 说明                       |
| --------------------------- | -------------------------- |
| `pygame.display.set_mode()` | 初始化游戏显示窗口         |
| `pygame.display.update()`   | 刷新屏幕内容显示，稍后使用 |

**`set_mode` 方法**

```python
set_mode(resolution=(0,0), flags=0, depth=0) -> Surface
```
### 4. 理解 **图像** 并实现图像绘制

* 在游戏中，能够看到的 **游戏元素** 大多都是 **图像**
    * **图像文件** 初始是保存在磁盘上的，如果需要使用，**第一步** 就需要 **被加载到内存**
* 要在屏幕上 **看到某一个图像的内容**，需要按照三个步骤：
    1. 使用 `pygame.image.load()` **加载图像的数据**
    2. 使用 **游戏屏幕** 对象，调用 `blit` 方法 将图像绘制到指定位置
    3. 调用 `pygame.display.update()` 方法更新整个屏幕的显示![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812193506114.png)
    4. **透明图像**
* `png` 格式的图像是支持 **透明** 的
* 在绘制图像时，**透明区域** 不会显示任何内容
* 但是如果**下方已经有内容**，会 **透过** **透明区域** 显示出来
### 5. 游戏中的动画实现原理

* 跟 **电影** 的原理类似，游戏中的动画效果，本质上是 **快速** 的在屏幕上绘制 **图像**
  
    * 电影是将多张 **静止的电影胶片** **连续、快速**的播放，产生连贯的视觉效果！
* 一般在电脑上 **每秒绘制 60 次**，就能够达到非常 **连续** **高品质** 的动画效果
    * 每次绘制的结果被称为 **帧 Frame**
    
    > **游戏循环的开始** 就意味着 **游戏的正式开始**

#### 游戏循环的作用
1. 保证游戏 **不会直接退出**
2. **变化图像位置** —— 动画效果
    * 每隔 `1 / 60 秒` 移动一下所有图像的位置
    * 调用 `pygame.display.update()` 更新屏幕显示
3. **检测用户交互** —— 按键、鼠标等...![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812193937291.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2k2MjIzNjcx,size_16,color_FFFFFF,t_70)
#### 游戏时钟

* `pygame` 专门提供了一个类 `pygame.time.Clock` 可以非常方便的设置屏幕绘制速度 —— **刷新帧率**
* 要使用 **时钟对象** 需要两步：
    * 1）在 **游戏初始化** 创建一个 **时钟对象**
    * 2）在 **游戏循环** 中让时钟对象调用 `tick(帧率)` 方法 
* `tick` 方法会根据 **上次被调用的时间**，自动设置 **游戏循环** 中的延时

### 6. 在游戏循环中 监听 事件 

#### 事件 `event`

* 就是游戏启动后，**用户针对游戏所做的操作**
* 例如：**点击关闭按钮**，**点击鼠标**，**按下键盘**...

#### 监听

* 在 **游戏循环** 中，判断用户 **具体的操作**

> 只有 **捕获** 到用户具体的操作，才能有针对性的做出响应

#### 代码实现

* `pygame` 中通过 `pygame.event.get()` 可以获得 **用户当前所做动作** 的 **事件列表**
    * 用户可以同一时间做很多事情
* 提示：**这段代码非常的固定**，几乎所有的 `pygame` 游戏都 **大同小异**！
```python
# 游戏循环
while True:

    # 设置屏幕刷新帧率
    clock.tick(60)

    # 事件监听
    for event in pygame.event.get():

        # 判断用户是否点击了关闭按钮
        if event.type == pygame.QUIT:
            print("退出游戏...")

            pygame.quit()

            # 直接退出系统
            exit()
```
### 7. 理解 **精灵** 和 **精灵组**

####   精灵 和 精灵
* 为了简化开发步骤，`pygame` 提供了两个类
    * `pygame.sprite.Sprite` —— 存储 **图像数据 image** 和 **位置 rect** 的 **对象**
    * `pygame.sprite.Group`
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812194401732.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2k2MjIzNjcx,size_16,color_FFFFFF,t_70)

#### 精灵
* 在游戏开发中，通常把 **显示图像的对象** 叫做精灵 `Sprite`
* **精灵** 需要 有 **两个重要的属性**
    * `image` 要显示的图像
    * `rect` 图像要显示在屏幕的位置
* 默认的 `update()` 方法什么事情也没做
    * 子类可以重写此方法，在每次刷新屏幕时，更新精灵位置

* **注意**：`pygame.sprite.Sprite` 并没有提供 `image` 和 `rect` 两个属性
    * 需要程序员从 `pygame.sprite.Sprite` 派生子类
    * 并在 **子类** 的 **初始化方法** 中，设置 `image` 和 `rect` 属性
#### 精灵组

* 一个 **精灵组** 可以包含多个 **精灵** 对象
* 调用 **精灵组** 对象的 `update()` 方法
    * 可以 **自动** 调用 **组内每一个精灵** 的 `update()` 方法
* 调用 **精灵组** 对象的 `draw(屏幕对象)` 方法
    * 可以将 **组内每一个精灵** 的 `image` 绘制在 `rect` 位置

##  整体框架


![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812204635623.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2k2MjIzNjcx,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190812195004347.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2k2MjIzNjcx,size_16,color_FFFFFF,t_70)
# 三,实践中遇到的问题和解决办法
 ## 1.敌机死后,子弹连带的消失
 因为子弹组是敌军对象的成员,子弹不是
就是在主函数需要敌军的子弹再加到一个组,而且所有敌军的子弹加到一起更更新更加方便,这样不用担心敌机毁掉了,他们的子弹对象也访问不了了.
## 2.子弹和敌机多次撞击
由于播放爆炸动画采用的方法是被撞毁时,先不移除精灵组,然后更改该对象图片,知道图片轮完了才kill(),这就导致进行下一次循环,对象还没kill(),kill()了就不能进行轮播.
**思考一:**
撞毁的时候新建循环把爆炸图片画在屏幕上,
行不通,第循环一次只能更新一帧图片,如果你要更新多帧那么其他精灵就会静止.
**思考二:**
撞毁时候,先移除精灵组,然后用变量储存,进行最初更新的方法.实验证明可行.
## 3.进行了update却不显示
混淆draw和display.update
首先一个精灵的update方法让图像有改变
精灵组的draw方法调用screen的blit方法画到屏幕上
这时候屏幕画面残留在上一帧
只有display更新了才能看到
## 4. 想方设法把一个Sprite或者rect或者image进行清除操作
其实pygam你们只有贴上去,没有"撕下来"
想要看不见他,两种方法如果是精灵,skill()从所有精灵组里面删除,如果只是单纯的image和rect,直接从他们的list里面remove,这样就不会被blit,实际上屏幕在更新,如果你想要看到,就要画在在更新的每一帧上面,之后如果不再用到它,python自己会进行回收.

**同样的道理,如果希望一个坏人消失,最好的办法不是你去杀死他,而是从你所在的集体里面孤立排除他,这样你就再也见不到他了**



## 5. 为什么英雄死掉了,还是会发生碰撞检测
这是因为,虽然我们把英雄加入英雄队伍,但是队伍中英雄很少,为了方便我们碰撞的时候不是从队伍中取直接就用该英雄对象进行检测,这时候,英雄skill()了,但是rect并没有丢失,
记住skill(),只是把他从需要显示或者操作群体中把他删除了,但是这个对象并没有被立即回收,它的rect还是在,还能用于碰撞检测

## 6, 如何按键不放,移动不止
方向键监听有两种方式
**按一下**


     elif event.type ==pygame.KEYDOWN and event.key = = pygame.K_RIGHT:

**按下**
返回所有按键的元组，如果某个键被按下，对应的值会是1

    keys_pressed = pygame.key.get_pressed()
    #判断是否按下了方向键
     if keys_pressed[pygame.K_RIGHT]:

## 7,不知道全局变量如何使用
python里面的全局常量和其他语言一样是没有歧义的,但是全局变量就不一样了,因为python定义变量不用定义类型,只有在赋值的时候才知道,所以在函数里面使用全局变量,无法保证两个变量是一样的,所以在函数里面需要用global声明一下这个变量是我开始设的这个全局变量,不是又重新定义了一个局部变量,

同样的道理,全局变量也不能跨模块调用,即使import了也只能用他的初始值,所以可以建立一个全局变量操作类,用来获取和修改全局变量.


## 8.明明画在屏幕上也更新了可就是看不到
注意更新的顺序影响图像的上下层关系

# 三,源代码
## 注释超级详细
## 方法比较简单,很容易看懂
## 易修改,易扩展,可定制化参数

```python
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

```

```python
import sys
import pygame

pygame.init()
from plane_sprites import *
# **************************************************************
# FileName: plane_main.py***************************************
# Author:  Junieson *********************************************
# Version:  2019.8.12 ******************************************
# ****************************************************************
class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化")

        # 1. 创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 创建结束界面
        self.canvas_over = CanvasOver(self.screen)
        # 2. 创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3. 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        # 分数对象
        self.score = GameScore()
        # 程序控制指针
        self.index = 0
        # 音乐bgm
        self.bg_music = pygame.mixer.Sound("./music/game_music.ogg")
        self.bg_music.set_volume(0.3)
        self.bg_music.play(-1)
        # 游戏结束了吗
        self.game_over = False
        # 4. 设置定时器事件 - 创建敌机　1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, random.randint(1000, 2000))
        pygame.time.set_timer(HERO_FIRE_EVENT, 400)
        pygame.time.set_timer(BUFF1_SHOW_UP, random.randint(10000, 20000))
        pygame.time.set_timer(BUFF2_SHOW_UP, random.randint(20000, 40000))
        pygame.time.set_timer(ENEMY_FIRE_EVENT, 2000)

    def __create_sprites(self):

        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机的精灵组

        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        # 创建敌军子弹组
        self.enemy_bullet_group = pygame.sprite.Group()

        # 血条列表
        self.bars = []
        self.bars.append(self.hero.bar)

        # 创建buff组
        self.buff1_group = pygame.sprite.Group()

        # 创建假象boom组
        self.enemy_boom = pygame.sprite.Group()

        # bomb列表
        self.bombs = []

    def start_game(self):
        print("游戏开始...")

        while True:
            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2. 事件监听
            self.__event_handler()
            # 3. 碰撞检测
            self.__check_collide()
            # 4. 更新/绘制精灵组
            self.__update_sprites()

            # 是否要结束游戏

            if self.game_over:
                self.canvas_over.update()

            # 5. 更新显示
            pygame.display.update()

    def __event_handler(self):  # 事件检测

        if self.score.getvalue() > 200+500*self.index:
            self.boss = Boss()
            self.enemy_group.add(self.boss)
            self.bars.append(self.boss.bar)
            self.index += 1

        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == CREATE_ENEMY_EVENT:
                # 创建敌机精灵将敌机精灵添加到敌机精灵组
                if self.score.getvalue() < 20:
                    enemy = Enemy()
                else:
                    if random.randint(0, 100) % 4:
                        enemy = Enemy()
                    else:
                        enemy = Enemy(2)

                self.enemy_group.add(enemy)
                self.bars.append(enemy.bar)

            elif event.type == HERO_FIRE_EVENT:
                for hero in self.hero_group:
                    hero.fire()
            elif event.type == BUFF1_SHOW_UP:
                buff1 = Buff1()
                self.buff1_group.add(buff1)
            elif event.type == BUFF2_SHOW_UP:
                if self.hero.bar.color == color_red:#按需分配
                    buff = Buff3()
                else:
                    buff= Buff2()
                self.buff1_group.add(buff)
            elif event.type == ENEMY_FIRE_EVENT:
                for enemy in self.enemy_group:
                    if enemy.number >= 2:
                        enemy.fire()
                        for bullet in enemy.bullets:
                            self.enemy_bullet_group.add(bullet)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bomb_throw()
            else:
                if self.game_over == True:
                    flag = self.canvas_over.event_handler(event)
                    if flag == 1:
                        self.__start__()
                    elif flag == 0:
                        pygame.quit()
                        sys.exit()

        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.heros_move(5)
        elif keys_pressed[pygame.K_LEFT]:
            self.heros_move(-5)
        elif keys_pressed[pygame.K_UP]:
            self.heros_move(0, -5)
        elif keys_pressed[pygame.K_DOWN]:
            self.heros_move(0, 5)
        else:
            self.heros_move(0, 0)

    def heros_move(self, x=0, y=0):
        self.hero.speedx = x
        self.hero.speedy = y

    def bomb_throw(self):
        music_use_bomb = pygame.mixer.Sound("./music/use_bomb.wav")
        if self.hero.bomb > 0:
            music_use_bomb.play()
            self.hero.bomb -= 1
            self.bombs.pop()
            for enemy in self.enemy_group:
                if enemy.number < 3:
                    enemy.bar.length = 0
                    enemy.isboom = True
                else:
                    enemy.injury = 20
                    enemy.isboom = True

    def __check_collide(self):

        # 1. 子弹摧毁敌机
        for enemy in self.enemy_group:
            for hero in self.hero_group:
                for bullet in hero.bullets:
                    if pygame.sprite.collide_mask(bullet, enemy):  # 这种碰撞检测可以精确到像素去掉alpha遮罩的那种哦
                        bullet.kill()
                        enemy.injury = bullet.hity
                        enemy.isboom = True
                        if enemy.bar.length <= 0:
                            self.enemy_group.remove(enemy)
                            self.enemy_boom.add(enemy)

        # 2. 敌机撞毁英雄
        for enemy in self.enemy_group:
            if pygame.sprite.collide_mask(self.hero, enemy):
                if enemy.number < 3:
                    enemy.bar.length = 0  # 敌机直接死
                    self.hero.injury = self.hero.bar.value / 4  # 英雄掉四分之一的血
                    if self.hero.buff1_num > 0:
                        self.hero.buff1_num -= 1
                        self.hero.music_degrade.play()
                    self.enemy_group.remove(enemy)
                    self.enemy_boom.add(enemy)
                    enemy.isboom = True
                else:
                    self.hero.bar.length = 0
                self.hero.isboom = True

        # 子弹摧毁英雄
        for bullet in self.enemy_bullet_group:
            if pygame.sprite.collide_mask(self.hero, bullet):
                bullet.kill()
                self.hero.injury = 1
                if self.hero.buff1_num > 0:
                    self.hero.music_degrade.play()
                    if self.hero.buff1_num == 5:
                        self.mate1.kill()
                        self.mate2.kill()
                    self.hero.buff1_num -= 1

                self.hero.isboom = True

        if not self.hero.alive():
            self.hero.rect.right = -10  # 把英雄移除屏幕
            if self.hero.buff1_num == 5:
                self.mate1.rect.right = -10
                self.mate2.rect.right = -10
            self.game_over = True

        # 3.buff吸收
        for buff in self.buff1_group:
            if pygame.sprite.collide_mask(self.hero, buff):
                buff.music_get.play()
                if buff.speedy == 1:  # 用速度来区分
                    if self.hero.buff1_num < 6:
                        self.hero.buff1_num += 1
                        self.hero.music_upgrade.play()
                        if self.hero.buff1_num == 5:
                            self.team_show()

                elif buff.speedy==2:
                    self.hero.bomb += 1
                    image = pygame.image.load("./images/bomb.png")
                    self.bombs.append(image)
                elif buff.speedy==3:
                    if self.hero.bar.length < self.hero.bar.weight*self.hero.bar.value:
                        self.hero.bar.length += self.hero.bar.weight*self.hero.bar.value
                buff.kill()

    def team_show(self):
        self.mate1 = Heromate(-1)
        self.mate2 = Heromate(1)
        self.mate1.image = pygame.image.load("./images/life.png")
        self.mate1.rect = self.mate1.image.get_rect()
        self.mate2.image = pygame.image.load("./images/life.png")
        self.mate2.rect = self.mate2.image.get_rect()
        self.hero_group.add(self.mate1)
        self.hero_group.add(self.mate2)

    # 各种更新
    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.enemy_boom.update()
        self.enemy_boom.draw(self.screen)

        self.heros_update()
        self.hero_group.draw(self.screen)

        for hero in self.hero_group:
            hero.bullets.update()
            hero.bullets.draw(self.screen)

        self.buff1_group.update()
        self.buff1_group.draw(self.screen)

        self.bars_update()
        self.bombs_update()

        self.enemy_bullet_group.update()
        self.enemy_bullet_group.draw(self.screen)

        self.score_show()

    def heros_update(self):
        for hero in self.hero_group:
            if hero.number == 1:
                hero.rect.bottom = self.hero.rect.bottom
                hero.rect.left = self.hero.rect.right
            if hero.number == -1:
                hero.rect.bottom = self.hero.rect.bottom
                hero.rect.right = self.hero.rect.left
            hero.update()

    def bars_update(self):
        for bar in self.bars:
            if bar.length > 0:
                bar.update(self.screen)
            else:
                self.bars.remove(bar)

    def bullet_enemy_update(self):
        for enemy in self.enemy_group:
            enemy.bullets.update()
            enemy.bullets.draw(self.screen)

    def bombs_update(self):
        i = 1
        for bomb in self.bombs:
            self.screen.blit(bomb, (0, 700 - (bomb.get_rect().height) * i))
            i += 1

    def score_show(self):
        score_font = pygame.font.Font("./STCAIYUN.ttf", 33)
        image = score_font.render("SCORE:" + str(int(self.score.getvalue())), True, color_gray)
        rect = image.get_rect()
        rect.bottom, rect.right = 700, 480
        self.screen.blit(image, rect)

    @staticmethod
    def __start__():
        # 创建游戏对象
        game = PlaneGame()

        # 启动游戏
        game.start_game()


if __name__ == '__main__':
    PlaneGame.__start__()

```

# 四, 总结和下载
这次的项目实践,让我对python面相对象程序设计有了更深的体会,也让我感受到了python语言简洁优雅的美感,如果你觉得还行的话,可以拿去小练一下手,如果有什么问题可以在评论区留言,我会在第一时间回复,
敲打不易,顺手点个赞吧,
（づ￣3￣）づ╭❤～.链接：https://pan.baidu.com/s/1QZ4jKe1KJaGdMYZyvvnecA 提取码：dndb 

























































 

 

 



 

 

 





##



 


​        
​	