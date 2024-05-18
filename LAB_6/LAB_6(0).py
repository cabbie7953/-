import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import random

pygame.init()

# цвета
black = (0, 0, 0)
white = (255, 255, 255)
dark_blue = (0, 0, 200)
burlywood_act = (255, 211, 155)
burlywood_noact = (205, 170, 125)
dark_red = (200, 0, 0)
dark_green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)

# окно
display_width = 500
display_height = 800
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Fruit Catcher")

# изображения
basket_img = pygame.image.load('mel.png')
basket_img = pygame.transform.scale(basket_img, (200, 150))
bg_images = ['room1.jpg', 'room2.jpg', 'room3.jpg']
bg = pygame.image.load(bg_images[0])
bomb_img = pygame.image.load('cockroach.png')
bomb_img = pygame.transform.scale(bomb_img, (100, 100))

clock = pygame.time.Clock()

game_over_sound = pygame.mixer.Sound("over.mp3")

class Basket(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.hitbox = (self.x, self.y + 20, 150, 80)

    def draw(self, window):
        window.blit(basket_img, (self.x, self.y))
        self.hitbox = (self.x, self.y + 20, 150, 80)

class Fruits(object):
    def __init__(self, x, y, f_type):
        self.x = x
        self.y = y
        self.f_type = f_type
        self.hitbox = (self.x, self.y, 100, 100)

    def draw(self, window):
        if self.f_type == 0:
            fruit = pygame.image.load('kfs.png')
            self.vel = 10
        fruit = pygame.transform.scale(fruit, (100, 100))
        window.blit(fruit, (self.x, self.y))
        self.hitbox = (self.x, self.y, 100, 100)

class Bombs(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.hitbox = (self.x, self.y, 100, 100)

    def draw(self, window):
        window.blit(bomb_img, (self.x, self.y))
        self.hitbox = (self.x, self.y, 100, 100)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, x, y, size):
    regText = pygame.font.Font("freesansbold.ttf", size)
    textSurf, textRect = text_objects(msg, regText)
    textRect.center = (x, y)
    window.blit(textSurf, textRect)

def button(msg, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if (x + width > mouse[0] > x and y + height > mouse[1] > y):
        pygame.draw.rect(window, active_color, (x, y, width, height))
        if (click[0] == 1 and action != None):
            if (action == "play"):
                main()
            elif (action == "quit"):
                pygame.quit()
                quit()
            elif (action == "instructions"):
                help_page()
            elif (action == "back"):
                game_intro()
            elif (action == "exit_game"):
                pygame.quit()
                quit()
            elif (action == "background"):
                background_selection()
            elif action in ["room1", "room2", "room3"]:
                set_background(action)
    else:
        pygame.draw.rect(window, inactive_color, (x, y, width, height))
    message_to_screen(msg, (x + (width / 2)), (y + (height / 2)), 20)

def set_background(bg_choice):
    global bg
    if bg_choice == "room1":
        bg = pygame.image.load(bg_images[0])
    elif bg_choice == "room2":
        bg = pygame.image.load(bg_images[1])
    elif bg_choice == "room3":
        bg = pygame.image.load(bg_images[2])


def background_selection():
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        window.fill(white)
        message_to_screen("Выберите фон", 250, 200, 50)
        button("Фон 1", 100, 300, 100, 50, dark_blue, bright_blue, "room1")
        button("Фон 2", 200, 300, 100, 50, dark_blue, bright_blue, "room2")
        button("Фон 3", 300, 300, 100, 50, dark_blue, bright_blue, "room3")
        button("Назад", 200, 500, 100, 50, burlywood_noact, burlywood_act, "back")
        pygame.display.update()
        clock.tick(15)

def help_page():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        window.fill(white)
        message_to_screen("КАК ИГРАТЬ", 250, 200, 50)
        message_to_screen("Используйте клавиши со стрелками", 250, 270, 20)
        message_to_screen("влево и вправо", 250, 300, 20)
        message_to_screen("для перемещения корзины", 250, 330, 20)
        message_to_screen("Соберите как можно больше еды,", 250, 410, 20)
        message_to_screen("но избегайте тараконов!", 250, 440, 20)
        message_to_screen("Пойманная еда: +2", 250, 520, 20)
        message_to_screen("Не пойманная еда: -1", 250, 550, 20)
        button("Назад", 100, 600, 75, 50, burlywood_noact, burlywood_act, "back")
        pygame.display.update()
        clock.tick(15)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        window.blit(bg, (0, 0))
        message_to_screen("Помоги Мелстрою", 250, 200, 50, )
        message_to_screen("Выжить в общаге", 250, 255, 30)
        button("Играть", 30, 450, 100, 50, dark_green, bright_green, "play")
        button("Выход (зачем?)", 300, 450, 170, 50, dark_red, bright_red, "quit")
        button("Как играть", 150, 450, 130, 50, burlywood_noact, burlywood_act, "instructions")
        button("Выбор фона", 150, 520, 130, 50, dark_blue, bright_blue, "background")
        pygame.display.update()
        clock.tick(15)

def main():
    score = 0
    fruits = []
    bombs = []
    fruit_add_counter = 0
    bomb_add_counter = 0
    add_fruit_rate = 30
    add_bomb_rate = 100
    basket = Basket(display_width * 0.5, display_height - 200)
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket.x > basket.vel - 5:
            basket.x -= basket.vel
        elif keys[pygame.K_RIGHT] and basket.x < 500 - 150 - basket.vel:
            basket.x += basket.vel
        window.blit(bg, (0, 0))
        fruit_add_counter += 1
        bomb_add_counter += 1
        if fruit_add_counter == add_fruit_rate:
            fruit_add_counter = 0
            f_startx = random.randrange(100, display_width - 100)
            f_starty = 0
            f_type = 0  # change to random later
            new_fruit = Fruits(f_startx, f_starty, f_type)
            fruits.append(new_fruit)
        if bomb_add_counter == add_bomb_rate:
            bomb_add_counter = 0
            b_startx = random.randrange(100, display_width - 100)
            b_starty = 0
            new_bomb = Bombs(b_startx, b_starty)
            bombs.append(new_bomb)
        for item in fruits:
            item.draw(window)
            item.y += item.vel
            if item.y > display_height:
                score -= 1
                print("Счет:", score)
                fruits.remove(item)
                if score < 0:
                    game_over()
        for item in fruits[:]:
            if (item.hitbox[0] >= basket.hitbox[0] - 20) and (item.hitbox[0] <= basket.hitbox[0] + 70):
                if basket.hitbox[1] - 120 <= item.hitbox[1] <= basket.hitbox[1] - 40:
                    fruits.remove(item)
                    score += 2
                    if item.f_type == 0:
                        score += 0
                    print("Счет:", score)
        for item in bombs:
            item.draw(window)
            item.y += item.vel
        for item in bombs[:]:
            if (item.hitbox[0] >= basket.hitbox[0]) and (item.hitbox[0] <= basket.hitbox[0] + 50):
                if basket.hitbox[1] - 120 <= item.hitbox[1] <= basket.hitbox[1] - 40:
                    game_over()
        message_to_screen("Счет: " + str(score), 50, 30, 20)
        basket.draw(window)
        pygame.display.update()
        clock.tick(60)

        def game_over():
            f = 1
            paused = True
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                while f == 1:
                    game_over_sound.play()
                    f = 0
                window.fill(white)
                message_to_screen("Игра окончена( ", 80, 30, 20)
                message_to_screen("Твой счет: " + str(score), 80, 70, 20)
                button("Выйти в главное меню", 100, 300, 250, 50, dark_red, bright_red, action="back")
                button("Выйти из игры", 100, 500, 250, 50, dark_red, bright_red, action="exit_game")
                pygame.display.update()

    pygame.quit()

game_intro()
