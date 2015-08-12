#coding:'utf-8'

#python 3.3.3
import pygame
from pygame.locals import *
from time import sleep
import sys
import random

#开始游戏
def start():
    pygame.init()
    width,height = 480,640
    screen = pygame.display.set_mode((width,height),0,32)
    pygame.display.set_caption('一起打飞机V1.0~~~')
    welcome = pygame.image.load('images/welcome/welcome.jpg').convert()
    fly = []
    fly.append(pygame.image.load('images/welcome/game_loading1.png').convert_alpha())
    fly.append(pygame.image.load('images/welcome/game_loading2.png').convert_alpha())
    fly.append(pygame.image.load('images/welcome/game_loading3.png').convert_alpha())
    flag = True
    while flag:
        for i in range(3):
            screen.blit(welcome, (0,0))
            screen.blit(fly[i],(160,450))
            pygame.display.update()
            sleep(0.5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    flag = False
                    break
    return screen
def game_over(screen):
    text = font.render("Game Over", 1, (0, 0, 0))
    screen.blit(text, (140, 280))
    pygame.display.update()
    
def check_bb(bullet,badguy):#检查子弹和敌机是否碰撞 
    if (bullet.x + bullet.image.get_width()*0.7 > badguy.x) and (bullet.x + bullet.image.get_width()*0.3 < badguy.x + badguy.image.get_width()) and (bullet.y < badguy.y + badguy.image.get_height()):
        return True
    return False

def check_hit(bad,plane):#检查飞机和敌机是否碰撞 检查UFO与飞机是否相撞
    if (plane.x + plane.image.get_width()*0.7 > bad.x) and (plane.x + plane.image.get_width()*0.3 < bad.x + bad.image.get_width()) and (plane.y + 0.7 * plane.image.get_height() > bad.y) and (plane.y + 0.3 * plane.image.get_width() < bad.y + bad.image.get_height()):
        return True
    return False
class Plane:
    def __init__(self,img_p):
        self.type = 1 #飞机类型 导弹数目
        self.x = 240
        self.y = 500
        self.image = img_p[0]
        self.boom = False#爆炸状态
        self.i = 0#飞机切换
        self.count = 0#延时计数器
        self.j = 3#爆炸图片切换
        self.dead = False
    def move(self):
        self.count += 1
        if self.boom == True:#检查是否爆炸
            if self.count == 100:#检查是否需要显示爆炸动画
                pygame.mixer.music.load('audio/baddead1.wav')
                pygame.mixer.music.play()
                self.count = 0
                self.image = img_p[self.j]
                self.j += 1
                if self.j == 6:#动画加载完毕
                    self.j = 3
                    self.dead = True
                    self.boom = False
        elif self.dead == False:#检查是否死亡
            if self.count == 100:#飞机喷射周期
                self.count = 0
                self.image = img_p[self.i]
                self.i += 1
                if self.i == 3:#从来
                    self.i = 0
            x,y = pygame.mouse.get_pos()
            x -= self.image.get_width()/2
            y -= self.image.get_height()/2#获取x y
            self.x = x
            self.y = y
class Bullets:
    def __init__(self,img_b):
        self.x = 0
        self.y = -1
        self.type = 0
        self.image = img_b[0]#子弹
        self.dead = True
    def move(self):
        if self.dead == False:
            self.y -= 0.3#子弹速度
        if self.y < 0:
            self.dead = True
    def reload(self):
        self.image = img_b[self.type]
        mx,my = pygame.mouse.get_pos()
        self.x = mx - self.image.get_width()/2
        self.y = my - self.image.get_height()/2#取 x y
        self.dead = False
class Ufo:
    def __init__(self,img_ufo):
        self.type = 0
        self.give = False
        self.img_temp = img_ufo
        self.reload(1)
    def reload(self,score):
        if score % 400 == 0:
            self.give = True
            #起始坐标
            self.x = random.randint(40,440)
            self.y = random.randint(-120, -70)
            self.type = random.randint(0,1)
            self.image = self.img_temp[self.type]
    def move(self):
        self.x_temp = random.randint(-4,4)/10
        self.x += self.x_temp
        if self.x < 20:
            self.x = 20
        if self.x > 460:
            self.x = 460
        self.y += 0.2
        if self.y > 640:
            self.give = False
            self.reload(1)
class Badguys:
    def __init__(self,img_bad):
        self.reload()#重载
    def move(self):
        if self.life <= 0:
            self.boom = True
        if self.boom:#如果爆炸
            self.count += 1
            if self.count == 150:#播放下一帧动画
                self.count = 0
                self.image = img_bad[self.type][self.i]
                self.i += 1
                if self.i == self.end:#结束
                    bgm_bad_3.stop()
                    bgm_bad_2.stop()
                    self.i = self.begin
                    self.boom = False
                    self.dead = True
                    self.reload()
        if self.y < 640:#是否在屏幕内
            self.y += self.speed
        else:
            self.reload()  
    def reload(self):
        self.dead = False
        self.boom = False
        switch = random.randint(0,100)
        if switch >20:
            self.type = 0
            self.life = 1
        elif switch > 5:
            self.type = 1
            self.life = 2
        else:
            self.type = 2
            self.life = 4
        if self.type == 2:
            self.image = img_bad[self.type][2]
            self.begin = 3
            self.end = 8
        else:
            self.begin = 2
            self.end = 6
            self.image = img_bad[self.type][1]
        self.i = self.begin
        self.count = 0
        self.x = random.randint(40,440)
        self.y = random.randint(-240,-60)#随机生成
        self.speed = 5/100 * (self.type+1)#计算速度
def load_plane(img_p):
    for i in range(1,7):
        path = 'images/game/plane'+str(i)+'.png'
        img_p.append(pygame.image.load(path).convert_alpha())
def load_badguys(img_bad):
    img_bad_1 = []
    img_bad_2 = []
    img_bad_3 = []
    for i in range(6):
        path = 'images/game/bad1'+str(i)+'.png'
        img_bad_1.append(pygame.image.load(path).convert_alpha())
    for i in range(6):
        path = 'images/game/bad2'+str(i)+'.png'
        img_bad_2.append(pygame.image.load(path).convert_alpha())
    for i in range(8):
        path = 'images/game/bad3'+str(i)+'.png'
        img_bad_3.append(pygame.image.load(path).convert_alpha())
    img_bad.append(img_bad_1)
    img_bad.append(img_bad_2)
    img_bad.append(img_bad_3)
    
###xif __name__ == '__main__':

screen = start()
pygame.mouse.set_visible(0)
#敌人图片
img_bad = []
#飞机图片
img_p = []
#子弹图片
img_b = []
#加载图片 设置字体
load_plane(img_p)
load_badguys(img_bad)
plane = Plane(img_p)
bg = pygame.image.load('images/game/bg.jpg').convert()
img_ufo=[]#UFO图片
img_ufo.append(pygame.image.load('images/game/ufo2.png').convert_alpha())
img_ufo.append(pygame.image.load('images/game/ufo1.png').convert_alpha())
img_b.append(pygame.image.load('images/game/bullet1.png').convert_alpha())
img_b.append(pygame.image.load('images/game/bullet2.png').convert_alpha())
img_bomb = pygame.image.load('images/game/bomb.png').convert_alpha()
font = pygame.font.Font('font/freesansbold.ttf',36)
bgm = pygame.mixer.Sound('audio/game_music.wav')
bgm_over= pygame.mixer.Sound('audio/game_over.wav')
bgm_bad_1= pygame.mixer.Sound('audio/baddead1.wav')
bgm_bad_2= pygame.mixer.Sound('audio/baddead2.wav')
bgm_bad_3= pygame.mixer.Sound('audio/baddead3.wav')
bgm_bullet= pygame.mixer.Sound('audio/bullet1.wav')
bgm_ufo= pygame.mixer.Sound('audio/get_ufo.wav')

bgm.play(loops = -1)
#初始化 是否射击 敌人数目 子弹数目 分数
ufo = Ufo(img_ufo)
shoot = False
num_bad = 10
num_b = 5
bullets = []
badguys = []
score = 0
for i in range(num_b):
    bullets.append(Bullets(img_b))
for i in range(num_bad):
    badguys.append(Badguys(img_bad))
#背景移动起始Y
bg_y = -640
#计数器
count = 0
over = 0
bomb_num = 0
all_dead = False
while True:
    #buff生命周期
    if count >= 50:
        count = 0
        if bullets[0].type == 1:
            for i in bullets:
                i.type = 0
    #获取事件并处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            press = pygame.mouse.get_pressed()
            for index in (range(len(press))):
                if press[index]:
                    if index == 0:
                         shoot = True
                         break
                    elif index == 2:
                        all_dead = True
                        break
            if shoot == True or all_dead == True:
                break
    #全部消灭
    if all_dead and bomb_num > 0:
        all_dead = False
        bomb_num -= 1
        for i in badguys:
            i.boom = True
    #游戏结束
    if plane.dead:
        over += 1
        if over == 1:
            over = 1
            bgm.stop()
            bgm_over.play()
            game_over(screen)
        continue
    screen.blit(bg, (0,bg_y))
    #背景运动
    bg_y += 0.1
    if bg_y >=0:
        bg_y = -640
    #射击后
    if shoot:
        shoot = False
        for each in bullets:
            if each.dead == True:
                if each.type == 1:
                    count += 1
                bgm_bullet.play()
                each.reload()
                break
    #判断子弹生命
    for i in bullets:
        if i.dead == False:
            #判断是否打到敌机
            for bad in badguys:
                if check_bb(i,bad) and bad.boom == False:
                    bad.life -= (i.type*2+1)
                    bgm_bad_1.play()
                    i.dead = True
                    score += 10 * (bad.type+1)
                    ufo.reload(score)
                    bgm_bad_3.play()
                    break
            # 子弹移动
            i.move()
            screen.blit(i.image,(i.x,i.y))
    #是否需要释放UFO
    if ufo.give == True:
        ufo.move()
        if check_hit(ufo,plane):
            bgm_ufo.play()
            if ufo.type == 1:
                for i in bullets:
                    i.type = 1
            else:
                bomb_num += 1
            ufo.give = False
            ufo.reload(1)
        screen.blit(ufo.image,(ufo.x, ufo.y))
    #检查敌机状态
    for bad in badguys:   
        if bad.boom == False and check_hit(bad,plane):
            bad.life -= 1
            bgm_bad_1.play()
            plane.boom = True
        #敌机移动
        bad.move()
        screen.blit(bad.image,(bad.x,bad.y))
    #飞机移动
    plane.move()
    #刷新屏幕
    screen.blit(img_bomb, (0, 560))
    text = font.render(" X  %d" % bomb_num, 1, (0, 0, 0))
    screen.blit(text, (60, 580))
    text = font.render("Score: %d" % score, 1, (0, 0, 0))
    screen.blit(text, (0, 0))
    screen.blit(plane.image,(plane.x,plane.y))
    pygame.display.update()
                





















        
