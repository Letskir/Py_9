from pygame import *

from random import randint
# Инициализация Pygame
font.init()
mixer.init()

# Настройки окна
window = display.set_mode((1366, 755))
bg = transform.scale(image.load("ddd.jpg"), (1366, 755))
mixer.music.load("Terraria.ogg")
mixer.music.play()

# Шрифты
font1 = font.Font("Comic Sans MS.ttf", 70)
font2 = font.Font("Comic Sans MS.ttf", 30)
lose=font1.render("You were slain...", False, (187,22,43))
lose2=font1.render("You were slain...", False, (0,0,0))
lose3=font1.render("You were slain...", False, (0,0,0))
win=font1.render("You win", False, (22,187,43))

  
music_hurt=mixer.Sound("hurt.mp3")
music_hurt.set_volume(0.1)
# Переменные
game = True
clock = time.Clock()
FPS = 60
game_started = False

# Лор игры
ready_text = font2.render("Нажмите 'Готово' для начала!", True, (187,22,43))
#для анимации персонажа
guide_r=[transform.scale(image.load("r/G_right.png"),(40,56)),
         transform.scale(image.load("r/G_right1.png"),(40,56)),
         transform.scale(image.load("r/G_right2.png"),(40,56)),
         transform.scale(image.load("r/G_right3.png"),(40,56)),
         transform.scale(image.load("r/G_right4.png"),(40,56)),
         transform.scale(image.load("r/G_right5.png"),(40,56)),
         transform.scale(image.load("r/G_right6.png"),(40,56)),
         transform.scale(image.load("r/G_right7.png"),(40,56))]
anim_r=0
guide_l=[transform.scale(image.load("l/G_left.png"),(40,56)),
         transform.scale(image.load("l/G_left1.png"),(40,56)),
         transform.scale(image.load("l/G_left2.png"),(40,56)),
         transform.scale(image.load("l/G_left3.png"),(40,56)),
         transform.scale(image.load("l/G_left4.png"),(40,56)),
         transform.scale(image.load("l/G_left5.png"),(40,56)),
         transform.scale(image.load("l/G_left6.png"),(40,56)),
         transform.scale(image.load("l/G_left7.png"),(40,56))]
anim_l=0

# Класс для спрайтов

class GameSprite(sprite.Sprite):    
    def __init__(self,im, speed,x,y,w,h):
        super().__init__()           
        self.image=transform.scale(image.load(im),(w,h))
        self.speed=speed
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

# Класс игрока
class Player(GameSprite):
    def update(self):
        global anim_r, anim_l
        keys=key.get_pressed()
        napravlenie="right"
        if keys[K_LEFT] and self.rect.x>10:
            if anim_l <=7:
                window.blit(guide_l[anim_l],(self.rect.x, self.rect.y))
                anim_l+=1
            else:
                anim_l=0
                window.blit(guide_l[anim_l],(self.rect.x, self.rect.y))
            self.rect.x-=self.speed
            napravlenie="left"
            if self.check_collision():
                self.rect.x+=self.speed
                music_hurt.play()


        elif keys[K_RIGHT] and self.rect.x<1360:
            if anim_r <=7:
                window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
                anim_r+=1
            else:
                anim_r=0
                window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
            self.rect.x+=self.speed
            if self.check_collision():
                self.rect.x-=self.speed
                music_hurt.play()
            napravlenie="right"  

        elif keys[K_UP] and self.rect.y>10 and sprite.collide_rect(gg,btn_restart)!=True:
            if napravlenie=="right":
                if anim_r <=7:
                    window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
                    anim_r+=1
                else:
                    anim_r=0
                    window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
            if napravlenie=="left":
                if anim_l <=7:
                    window.blit(guide_l[anim_l],(self.rect.x, self.rect.y))
                    anim_l+=1
                else:
                    anim_l=0
                    window.blit(guide_l[anim_l],(self.rect.x, self.rect.y)) 
            self.rect.y-=self.speed
            if self.check_collision():
                self.rect.y+=self.speed
                music_hurt.play()


        elif keys[K_DOWN]and self.rect.y<750:
            if napravlenie=="right":
                if anim_r <=7:
                    window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
                    anim_r+=1
                else:
                    anim_r=0
                    window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
            if napravlenie=="left":
                if anim_l <=7:
                    window.blit(guide_l[anim_l],(self.rect.x, self.rect.y))
                    anim_l+=1
                else:
                    anim_l=0
                    window.blit(guide_l[anim_l],(self.rect.x, self.rect.y)) 
            self.rect.y+=self.speed
            if self.check_collision():
                self.rect.y-=self.speed
                music_hurt.play()
            self.check_spike_collision()
                
        else:
            self.reset()
    def check_collision(self):
        for wall in walls:
            if sprite.collide_rect(self, wall):
                return True
        return False
    def check_spike_collision(self):
        if sprite.spritecollideany(self, spikes):  # Проверяем столкновение с любыми шипами
            music_hurt.play()
            self.rect.x = 50  # Отправляем игрока на старт
            self.rect.y = 100

# Класс врагов


class Enemy(GameSprite):
    def __init__(self, lim, rim, speed, x, y, w, h):
        super().__init__(lim, speed, x, y, w, h)
        self.picl = transform.scale(image.load(lim), (w, h))
        self.picr = transform.scale(image.load(rim), (w, h))
        self.image = self.picl  # Начальное изображение
        self.direction = "l"

    def update(self):
        if self.direction == "l":
            self.rect.x -= self.speed
            self.image = self.picl  # Устанавливаем изображение для движения влево
        else:
            self.rect.x += self.speed
            self.image = self.picr  # Устанавливаем изображение для движения вправо

        # Проверка границ и изменение направления
        if self.rect.x >= 1000:
            self.direction = "l"
        elif self.rect.x <= 200:
            self.direction = "r"

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))  # Отображаем текущее изображение врага
# Класс стен

class Wall(sprite.Sprite):
    def __init__(self, color_1,color_2,color_3,wall_width,wall_height,x,y):
        super().__init__()
        self.color_1=color_1
        self.width=wall_width
        self.height=wall_height
        self.image=Surface((self.width,self.height))
        self.image.fill((color_1,color_2,color_3))
        self.rect=self.image.get_rect()
        self.rect.x=x 
        self.rect.y=y
    def draw_wall(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
monstr=Enemy("Scutlix.png", "Scutlix_r.png", 4, 400, 240, 250, 168)
gg=Player("r/G_right.png",4,50,100,40,56)
win_item=GameSprite("win_item.png",0,50,600,50,50)
btn_restart=GameSprite("btn.png",0,0,0,150,75)


# Переменные для жизни игрока
finish=False
x,y=-1,-1
# Создание объектов игры
walls = [
    Wall(230, 23, 32, 1200, 100, 0, 400),
    Wall(230, 23, 32, 400, 250, 150, 0),
    Wall(230, 23, 32, 730, 250, 650, 0),
    Wall(230, 23, 32, 400, 150, 550, 0),
    
]

# Начальное окно с лором
def start_menu():
    while True:
        window.fill((0, 0, 0))  # Чёрный фон

        # Отображение текста лора
        font_start = font.Font(None, 36)
        lore_text = [
            "Вы - последний житель мира Terraria, на который прилитело марсианское безумие.",
            "Но скоро будет прибыть Истинный глаз Ктулху, который уничтожит весь мир.",
            "Вам нужно пройти через лабиринт и собрать ключ от управления НЛО.",
            "Он вам поможет защититься от Истинных глаз Ктулху.",
            "Нажмите 'Готово', чтобы начать."
        ]
        
        for i, line in enumerate(lore_text):
            text_surface = font_start.render(line, True, (255, 255, 255))
            window.blit(text_surface, (50, 50 + i * 30))

        # Кнопка "Готово"
        btn_ready = font_start.render("Готово", True, (255, 0, 0))
        btn_rect = btn_ready.get_rect(center=(360, 400))
        window.blit(btn_ready, btn_rect)

        for ev in event.get():
            if ev.type == QUIT:
                quit()
            if ev.type == MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(ev.pos):
                    return  # Переход к игре

        display.update()
# Класс шипов
class Spike(GameSprite):
    def __init__(self, image_path, x, y, scale=3):  
        original_width = 30
        original_height = 48
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        super().__init__(image_path, 0, x, y, new_width, new_height)

# Группа для шипов
spikes = sprite.Group()

# Координаты для шипов
spike_positions = [
    (200, 500, "Tesla_Turret_reversed.gif"), 
    (600, 500, "Tesla_Turret_reversed.gif"), 
    (1000, 500, "Tesla_Turret_reversed.gif"),  # Используем перевёрнутую картинку
    (400, 630, "Tesla_Turret.gif"), 
    (800, 630, "Tesla_Turret.gif"), 
    (1200, 630, "Tesla_Turret.gif")   # Обычные шипы
]

# Создаём шипы с разными изображениями
for x, y, image_path in spike_positions:
    spike = Spike(image_path, x, y, scale=3)
    spikes.add(spike)

start_menu()
# Основной игровой цикл
while game:
    for ev in event.get():
        if ev.type == QUIT:
            game=False
        if ev.type==MOUSEBUTTONDOWN:
            x,y=ev.pos
        if btn_restart.rect.collidepoint(x, y):
            finish = False
            x, y = -1, -1  # Сбрасываем координаты клика
            gg.rect.x = 50  # Начальные координаты игрока
            gg.rect.y = 100
            mixer.music.load("Terraria.ogg")  # Перезапускаем музыку
            mixer.music.play()


    if sprite.collide_rect(gg,monstr):
        finish=True

        window.blit(lose2,(1366/3-2,755/3+2))
        window.blit(lose2,(1366/3+2, 755/3-2))
        window.blit(lose,(1366/3,755/3))
        
        mixer.music.play()
    
    if sprite.collide_rect(gg,win_item):
        finish=True
        window.blit(win,(150,150)) 
    if finish!=True :
        
        window.blit(bg,(0,0))
        btn_restart.reset()
        monstr.reset()
        monstr.update()
        gg.update()
        spikes.draw(window)  # Отображаем все шипы

        win_item.reset()
        
        for wall in walls:
            wall.draw_wall() # Отрисовка стен
        display.update() # Обновление экрана
    display.update()
    clock.tick(FPS)

    
quit()
#pyinstaller --onefile --icon=ufo.ico --noconsole main.py