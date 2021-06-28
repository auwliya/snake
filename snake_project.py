import pygame, sys, random, os
from pygame.constants import KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, QUIT
from pygame.math import Vector2

# Snake created by Auwliya123 / Lemon1
# All pixel art is created by me
# Special thanks to itscountvertigo for helping with some stuff

pygame.init()
mainClock = pygame.time.Clock()
pygame.display.set_caption('snake')
screen = pygame.display.set_mode((500, 500),0,32)

# four different sizes of fonts
font_title = pygame.font.Font('Font/ARCADECLASSIC.ttf',35)
font = pygame.font.Font('Font/ARCADECLASSIC.ttf',25)
font_small = pygame.font.Font('Font/ARCADECLASSIC.ttf',15)

# Graphics for the different screens
howtoplayscreen = pygame.image.load('Graphics/howtoplay.png').convert_alpha()
game_over_screen_image = pygame.image.load('Graphics/game_over_screen.png').convert_alpha()
you_won_screen = pygame.image.load('Graphics/youwon.png').convert_alpha()

# easter egg that gives you a 1% chance the sky is a different color
if random.randint(0,100) >= 1:
    Home_screen = pygame.image.load('Graphics/home.png').convert_alpha()
else:
    Home_screen = pygame.image.load('Graphics/home-easter-egg.png').convert_alpha()

def main_menu():
    click = False
    while True:
        screen = pygame.display.set_mode((500, 500),0,32)
        screen.fill((175,215,70))
        # Has the buttons, and blits the button design onto it
        # The buttons have individual blits, it helps me to check functionality of the buttons
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(200, 250, 100, 50)
        
        button_2 = pygame.Rect(150, 310, 200, 50)
        
        homescreen_rect = pygame.Rect(0, 0, 500, 500)
        screen.blit(Home_screen,homescreen_rect)
        
        pygame.display.update()
        mainClock.tick(60)
        
        # starts the game or  goes to How to play when pointer and the button are hovering over each other
        # the print hover shows that the mouse is currently capable of using the button (a tool to explain collidepoint)
        if button_1.collidepoint((mx, my)):
            #print('hover')
            if click:
                game()
        
        elif button_2.collidepoint((mx, my)):
            if click:
                How_to_play()

        # pygame and quit events, sets click to true making the buttons work
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

def game():
    while True:
        class SNAKE:
            def __init__(self):
                # Vectors the snake starts out with (three blocks long, always in the same coördinates)
                self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
                self.direction = Vector2(1,0)
                self.new_block = False

                # Snake graphics
                self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
                self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
                self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
                self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha() 

                self.tail_down = pygame.image.load('Graphics/tail_up.png').convert_alpha()   
                self.tail_up = pygame.image.load('Graphics/tail_down.png').convert_alpha()   
                self.tail_left = pygame.image.load('Graphics/tail_right.png').convert_alpha()   
                self.tail_right = pygame.image.load('Graphics/tail_left.png').convert_alpha()

                self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha() 
                self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

                self.body_tr = pygame.image.load('Graphics/body_right_up.png').convert_alpha()
                self.body_tl = pygame.image.load('Graphics/body_left_up.png').convert_alpha()
                self.body_br = pygame.image.load('Graphics/body_right_down.png').convert_alpha()
                self.body_bl = pygame.image.load('Graphics/body_left_down.png').convert_alpha()
                
                self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

            def draw_snake(self):
                # updates head and body parts so the blocks have the right sprites
                self.update_head_graphics()
                self.update_tail_graphics()

                for index,block in enumerate(self.body):
                    # what direction is it going in
                    # make a rectangle for positioning
                    x_pos = int(block.x * cell_size)
                    y_pos = int(block.y * cell_size)
                    block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

                    if index == 0:
                        screen.blit(self.head,block_rect)
                    elif index == len(self.body) - 1:
                        screen.blit(self.tail,block_rect)
                    else:
                        # if the if and elif dont apply, its a corner piece, so only figuring out the oriëntation works
                        previous_block = self.body[index + 1] - block
                        next_block = self.body[index - 1] - block
                        if previous_block.x == next_block.x:
                            screen.blit(self.body_vertical,block_rect)
                        elif previous_block.y == next_block.y:
                            screen.blit(self.body_horizontal,block_rect)
                        else:
                            if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                                screen.blit(self.body_tl,block_rect)
                            elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                                screen.blit(self.body_bl,block_rect) 
                            elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                                screen.blit(self.body_tr,block_rect)
                            elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                                screen.blit(self.body_br,block_rect)

            def update_head_graphics(self):
                # update head and tail graphics figure out what sprite to blit onto the block
                # by subtracting the head from the first body after it you get the direction the head is heading in
                head_relation = self.body[1] - self.body[0]
                if head_relation == Vector2(1,0): self.head = self.head_left
                elif head_relation == Vector2(-1,0): self.head = self.head_right
                elif head_relation == Vector2(0,1): self.head = self.head_up
                elif head_relation == Vector2(0,-1): self.head = self.head_down

            def update_tail_graphics(self):
                # works the same as update_head_graphics
                tail_relation = self.body[-2] - self.body[-1]
                if tail_relation == Vector2(1,0): self.tail = self.tail_left
                elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
                elif tail_relation == Vector2(0,1): self.tail = self.tail_up
                elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

            def move_snake(self):
                # adds a block, sets self.new_block to false again
                if self.new_block == True:
                    body_copy = self.body[:]
                    body_copy.insert(0,body_copy[0] + self.direction)
                    self.body = body_copy[:]
                    self.new_block = False
                else:
                    # moves the snake forward in the direction 
                    body_copy = self.body[:-1]
                    body_copy.insert(0,body_copy[0] + self.direction)
                    self.body = body_copy[:]

            def add_block(self):
                # sets new_block to true after collision
                self.new_block = True

            # cronch
            def play_crunch_sound(self):
                self.crunch_sound.play()

        class FRUIT:
            def __init__(self):
                # the fruit starts randomized
                self.fruit_sprite = apple
                self.x = random.randint(0,cell_number - 1)
                self.y = random.randint(0,cell_number - 1)
                self.pos = Vector2(self.x,self.y)

            def draw_fruit(self):
                # creates a rectangle for the apple, blit teleports the graphic onto the apple
                #The sprite it .blits onto it is set as self.fruit_sprite so it can be both an apple or a lemon
                fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
                screen.blit(self.fruit_sprite,fruit_rect)

            def randomize(self):
                # creates a random coördinate between 0 and 20 - 1 (so it doesn't go outside the border)
                # randomizes the fruit again after eating (__init__ only does it at the start)
                self.x = random.randint(0,cell_number - 1)
                self.y = random.randint(0,cell_number - 1)
                self.pos = Vector2(self.x,self.y)
                # if the random number is 1 or 2 its an apple, if its a 0 its a lemon.
                if random.randint(0,2) >= 1:
                    self.fruit_sprite = apple
                else:
                    self.fruit_sprite = lemon

        class MAIN:
            # contains all the other things like updates, drawings and checks so that it keeps getting repeated
            def __init__(self):
                # contains self.score (otherwise it keeps setting itself to 0)
                self.snake = SNAKE()
                self.fruit = FRUIT()
                self.score = 0
                self.lemons_consumed = 0
                self.apples_consumed = 0
            
            def update(self):
                self.snake.move_snake()
                self.check_collision()
                self.check_fail()

            def draw_elements(self):
                self.draw_grass()
                self.fruit.draw_fruit()
                self.snake.draw_snake()
                self.draw_score()
            
            def check_collision(self):
                if self.fruit.pos == self.snake.body[0]:
                # randomizes the fruit again, adds a block and adds a point to the score counter
                    self.snake.play_crunch_sound()
                    # different collisions with the fruits
                    if self.fruit.fruit_sprite == apple:
                        self.snake.add_block()
                        self.score += 1
                        self.apples_consumed += 1
                    elif self.fruit.fruit_sprite == lemon:
                        self.snake.add_block()
                        self.snake.add_block()
                        self.score += 2
                        self.lemons_consumed += 1
                    self.fruit.randomize()

                for block in self.snake.body[1:]:
                    # makes sure that the fruit cannot spawn below or on the snake
                    if block == self.fruit.pos:
                        self.fruit.randomize()

            def check_fail(self):
                # checks it the snake is between the allowed x and y values of the grid
                if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
                    self.game_over()
                
                for block in self.snake.body[1:]:
                    if block == self.snake.body[0]:
                        self.game_over()
                # epic fail

            def draw_grass(self):
                # only draws every other block using division\
                # row = rows, col = columns
                grass_color = (167,209,61)
                for row in range(cell_number):
                    if row % 2 == 0:
                        for col in range(cell_number):
                            if col % 2 == 0:
                                grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                                pygame.draw.rect(screen,grass_color,grass_rect)
                    else:
                        for col in range(cell_number):
                            if col % 2 != 0:
                                grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                                pygame.draw.rect(screen,grass_color,grass_rect)

            def game_over(self):
                # exits game and prints your score in powershell
                # extra info that doesn't show up in the game if you want to check how many you ate
                print(f"\nYour score was {self.score}!\n")
                if self.lemons_consumed >= 1:
                    print(f"You consumed {self.lemons_consumed} lemon(s)!")
                elif self.lemons_consumed == 0:
                    print(f"You didn't eat any lemons!")

                if self.apples_consumed >=1:
                    print(f"you consumed {self.apples_consumed} apple(s)!\n")
                elif self.apples_consumed == 0:
                    print(f"You didn't eat any apples!\n")
                
                # (self.score) brings the score over to the def game_over_screen
                game_over_screen(self.score)
            
            def draw_score(self):
                # draws the score in the corner of the screen
                score_surface = game_font.render(str(self.score),True,(56,74,12))
                score_x = int(cell_size * cell_number - 60)
                score_y = int(cell_size * cell_number - 60)
                score_rect = score_surface.get_rect(center = (score_x,score_y))
                screen.blit(score_surface,score_rect)

        pygame.init()
        cell_size = 40
        cell_number = 20
        screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
        clock = pygame.time.Clock() 

        # apple and lemon graphics
        apple = pygame.image.load('Graphics/apple.png').convert_alpha() 
        lemon = pygame.image.load('Graphics/lemon.png').convert_alpha() 

        # game_font can be replaced with font, but it works right now so im not changing the code haha
        main_game = MAIN()
        game_font = pygame.font.Font('Font/ARCADECLASSIC.ttf',25)

        SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(SCREEN_UPDATE,150)

        while True:
            # draw elements
            # snake cant go left when moving right etc.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == SCREEN_UPDATE:
                    main_game.update()

                # arrow controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0,-1)
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0,1)
                    if event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1,0)
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1,0)

                # WASD Controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0,-1)
                    if event.key == pygame.K_s:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0,1)
                    if event.key == pygame.K_a:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1,0)
                    if event.key == pygame.K_d:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1,0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()

            screen.fill((175,215,70))
            main_game.draw_elements()
            pygame.display.update()
            clock.tick(60)

def How_to_play():
    while True:
        screen.fill((175,215,70))
        # uses .blit to make the how to play screen look cool

        explanation_screen = pygame.Rect(0, 0, 500, 500)
        screen.blit(howtoplayscreen,explanation_screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()

        pygame.display.update()
        mainClock.tick(60)

def game_over_screen(score):
    click = False
    while True:
        screen = pygame.display.set_mode((500, 500),0,32)
        screen.fill((175,215,70))
        mx, my = pygame.mouse.get_pos()
        
        button_3 = pygame.Rect(200, 250, 100, 50) 
        button_4 = pygame.Rect(150, 310, 200, 50)
        
        # the names are long because its almost identical to the other score during the game
        game_over_screen_rect = pygame.Rect(0, 0, 500, 500)
        if score <= 396:
            screen.blit(game_over_screen_image,game_over_screen_rect)
        else:
            screen.blit(you_won_screen,game_over_screen_rect)
        
        score_game_over_surface = font_title.render(str(score),True,(0,0,0))
        score_rect = score_game_over_surface.get_rect(center = (420,213))
        screen.blit(score_game_over_surface,score_rect)

        pygame.display.update()
        mainClock.tick(60)

        if button_3.collidepoint((mx, my)):
            if click:
                game()
            
        elif button_4.collidepoint((mx, my)):
            if click:
                main_menu()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

#starts the menu when running the game
main_menu()