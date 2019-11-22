import pygame
import random
import os

pygame.mixer.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

sounds = []
sounds.append(pygame.mixer.Sound(r'music/eat.wav'))

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (0,255,0)
screen_width = 900
screen_height = 700
gameWindow = pygame.display.set_mode((screen_width,screen_height))

bg1 = pygame.image.load(r"images/welcome.png")
bg1 = pygame.transform.scale(bg1, (screen_width, screen_height)).convert_alpha()
bg2 = pygame.image.load(r"images/game.jpg")
bg2 = pygame.transform.scale(bg2, (screen_width, screen_height)).convert_alpha()
bg3 = pygame.image.load(r"images/gameover.jpg")
bg3 = pygame.transform.scale(bg3, (screen_width, screen_height)).convert_alpha()

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

def gameov(score,hscore,snk_list,snake_size,food_x,food_y):
    for i in range(0,7):
        #gameWindow.fill(white)
        gameWindow.blit(bg2,(0,0))
        pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size + 5, snake_size + 5])
        text_score("Score: " + str(score) + "    High Score: " + str(hscore), red, 2.5, 2.5)
        if i%2==0:
            plot_snk(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        pygame.time.delay(800)

def welcome():
    exit_game = False
    pygame.mixer.music.load(r'music/welcome.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(start=32.0)
    while not exit_game:
        #gameWindow.fill((233,220,229))
        gameWindow.blit(bg1,(0,0))
        text_score("Welcome to Snakes!!! ",yellow,300,300)
        text_score("Press Space Bar to play.. ",yellow,280,350)
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
    snake_x = 200
    snake_y = 150
    velocity_x = 0
    velocity_y = 0
    snk_list =[]
    v_init = 1
    snk_length = 1
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        hscore = f.read()
    food_x = random.randint(40, screen_width / 2)
    food_y = random.randint(40, screen_height / 2)

    snake_size = 25
    fps = 60
    score = 0

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(hscore))
            #gameWindow.fill((233,229,220))
            gameWindow.blit(bg3,(0,0))
            text_score("Your Score : "+str(score),yellow,380,300)
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
                v_init += 0.1
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 20
                if score > int(hscore):
                    hscore = score
            #gameWindow.fill(white)
            gameWindow.blit(bg2,(0,0))
            text_score("Score: " + str(score)+ "    High Score: "+str(hscore), red, 2.5, 2.5)
            pygame.draw.rect(gameWindow,red,[food_x, food_y, snake_size+5, snake_size+5])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                pygame.mixer.music.load(r'music/over.mp3')
                pygame.mixer.music.play()
                gameov(score,hscore,snk_list,snake_size,food_x,food_y)
                game_over = True


            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                pygame.mixer.music.load(r'music/over.mp3')
                pygame.mixer.music.play()
                gameov(score,hscore,snk_list,snake_size,food_x,food_y)
                game_over = True

            plot_snk(gameWindow,black,snk_list,snake_size)

        pygame.display.update()
        clock.tick()

    pygame.quit()
    quit()
welcome()
