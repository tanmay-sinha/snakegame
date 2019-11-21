import pygame
import random
import os

pygame.mixer.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

sounds = []
sounds.append(pygame.mixer.Sound(r'D:/gameproj/music/eat.wav'))

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255,255,0)
screen_width = 900
screen_height = 700
gameWindow = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("SAANP KA KHEL")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)


def text_score(text, color, x, y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text, [x, y])

def plot_snk(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,color,[x,y,snake_size,snake_size])

def welcome():
    exit_game = False
    pygame.mixer.music.load(r'music/welcome.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(start=32.0)
    while not exit_game:
        gameWindow.fill((233,220,229))
        text_score("Welcome to Snakes!!! ",black,300,300)
        text_score("Press Space Bar to play.. ",black,280,350)
        text_score("Press BACKSPACE to quit..", red, 270, 400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load(r'music/game.mp3')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(loops=-1)
                    gameloop()
                if event.key == pygame.K_BACKSPACE:
                    exit_game = True
        pygame.display.update()
        clock.tick(60)

def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    v_init = 0.5
    snk_list = []
    snk_length = 1
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        hscore = f.read()
    food_x = random.randint(40, screen_width / 2)
    food_y = random.randint(40, screen_height / 2)

    snake_size = 30
    fps = 60
    score = 0

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(hscore))
            gameWindow.fill((233,229,220))
            text_score("Game Over, Press ENTER to play again!",red,200,350)
            text_score("Press BACKSPACE to quit..",red,300,400)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        exit_game = True
                        welcome()
                    if event.key == pygame.K_BACKSPACE:
                        exit_game = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if velocity_x==0:
                            velocity_x = v_init
                            velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        if velocity_x == 0:
                            velocity_x = -v_init
                            velocity_y = 0
                    if event.key == pygame.K_UP:
                        if velocity_y==0:
                            velocity_y = -v_init
                            velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        if velocity_y == 0:
                            velocity_y = v_init
                            velocity_x = 0
            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x-food_x)<15 and abs(snake_y-food_y)<15:
                sounds[0].play()
                score += 10
                v_init += 0.05
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 20
                if score > int(hscore):
                    hscore = score
            gameWindow.fill(white)
            text_score("Score: " + str(score)+ "    High Score: "+str(hscore), red, 2.5, 2.5)
            pygame.draw.rect(gameWindow,red,[food_x,food_y,snake_size,snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load(r'music/over.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load(r'music/over.mp3')
                pygame.mixer.music.play()

            pygame.draw.rect(gameWindow,black,[snake_x,snake_y,snake_size,snake_size])
            plot_snk(gameWindow,black,snk_list,snake_size)

        pygame.display.update()
        clock.tick()

    pygame.quit()
    quit()
welcome()
