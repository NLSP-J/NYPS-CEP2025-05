import pygame as pg
import random, time
pg.init()
clock = pg.time.Clock()

black = (0, 0, 0)

win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Falling Debris')

font = pg.font.Font(None, 30)
font_gameover = pg.font.Font(None, 60)
speed = 10
score = 0
running = True
lives = 4
diff = 'easy'

player_size = 40
player_pos = [win_width / 2, win_height - player_size]  # 400, 600-40
player_image = pg.image.load('./assets/images/mario.png')
player_image = pg.transform.scale(player_image, (player_size, player_size))  # 40,40

obj_size = 60
obj_data = []     # List to store object positions and their images
obj = pg.image.load('./assets/images/e1.png')
obj = pg.transform.scale(obj, (obj_size, obj_size))

heart_size = 60
heart_data = []     
heart = pg.image.load('./assets/images/heart.png')
heart = pg.transform.scale(heart, (heart_size, heart_size))


bg_image = pg.image.load('./assets/images/background.png')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))


def create_object(obj_data):
    if len(obj_data) < 230 and random.random() < 0.1:    
        x = random.randint(0, win_width - obj_size)
        y = 0                                         
        obj_data.append([x, y, obj])

def create_heart(heart_data):
    if len(heart_data) < 2 and random.random() < 0.1:    
        x = random.randint(0, win_width - heart_size)
        y = 0                                         
        heart_data.append([x, y, heart])


def update_objects(obj_data):
    global score

    for object in obj_data:
        x, y, image_data = object
        if y < win_height:
            y += speed
            object[1] = y
            screen.blit(image_data, (x, y))
        else:
            obj_data.remove(object)
            score += 1

def update_hearts(heart_data):

    for heart in heart_data:
        x, y, image_data = heart
        if y < win_height:
            y += speed
            heart[1] = y
            screen.blit(image_data, (x, y))
        else:
            heart_data.remove(heart)

def inc_difficulty(score):

    global speed, diff, lives, score_inc
    if score < 15:
        speed = 20 
        diff = 'Easy'
        score_inc = 1
    
    elif score < 35 :
        speed = 30 
        diff = 'Med'
        score_inc = 0.5

    elif score < 60 :
        speed = 40
        diff = 'Hard'
        score_inc = 0.25
    
    elif score < 90 :
        speed = 55
        diff = 'Crazy'
        score_inc = 0.10
        
    elif score < 140 :
        speed = 70
        diff = 'BEAST'
        score_inc = 0.05

    elif score < 200 :
        speed = 90
        diff = 'GOD'
        score_inc = 0.02

    elif score < 400 :
        speed = 125
        diff = 'world record(?)'
        score_inc = 0.01

    elif score >= 400 :
        text = f'WOW!You survived the EMARGANCY!'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 10, win_height + 100))


def collision_check(obj_data, player_pos):
    global running, lives

    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(obj_rect):
            obj_data.remove(object)
            lives -= 1
            if lives == 0:
                text = f'Oh no! Game over!'
                text = font_gameover.render(text, 10, black)
                screen.blit(text, (player_x - 100, player_y - 60))
                pg.display.update()
                time.sleep(5)
                running = False
            break


def heart_collision_check(heart_data, player_pos):
    global running, lives

    for heart in heart_data:
        x, y, image_data = heart
        player_x, player_y = player_pos[0], player_pos[1]
        heart_rect = pg.Rect(x, y, heart_size, heart_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(heart_rect):
            heart_data.remove(heart)
            lives += 1
            break

def cap_lives():
    global lives

    if lives > 4 :
        lives = 4

def main():

    global running, player_pos

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                x, y = player_pos[0], player_pos[1]
                if event.key == pg.K_LEFT:
                    x -= 20
                elif event.key == pg.K_RIGHT:
                    x += 20
                player_pos = [x, y]

        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        text = f'Difficulty: {diff}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 240, win_height - 80))


        text = f'Score: {score}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 60))

        text = f'Lives: {lives}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 40))

        create_object(obj_data)
        inc_difficulty(score)
        create_heart(heart_data)
        update_objects(obj_data)
        update_hearts(heart_data)
        cap_lives()
        collision_check(obj_data, player_pos)
        heart_collision_check(heart_data, player_pos)

        clock.tick(30)
        pg.display.flip()

main()