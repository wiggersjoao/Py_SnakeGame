# import the pygame module, so you can use it
import pygame
import random
import math

SNAKE_SIZE = 32
SNAKE_INITIAL_X = 0
SNAKE_INITIAL_Y = 0
# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("snake.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Snake Game")
    pygame.font.init() 
    myfont = pygame.font.SysFont('Comic Sans MS', 15)
    failfont = pygame.font.SysFont('Comic Sans MS', 40)
    clock = pygame.time.Clock()
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((800,600))
    
    #player position
    player_x = 0
    player_y = 0
    global player_variation
    player_variation = [0,0]
    player_image = pygame.image.load("snake-head.png")
    player_body_image = pygame.image.load("black-square-shape.png")
    global snake_pos
    snake_pos = [(SNAKE_INITIAL_X,SNAKE_INITIAL_Y)]

    #food position
    global food_x
    global food_y
    food_x = 0
    food_y = 0 
    food_image = pygame.image.load("rat-silhouette.png")
    
    # define a variable to control the main loop
    global running 
    global flag_fail 
    running = True
    flag_fail = False

    #score
    score = 0
    
    #funcion for player
    def player():
        
        for i in range(len(snake_pos)-1,-1,-1):
            if i == 0:
                screen.blit(player_image,(snake_pos[0][0],snake_pos[0][1]))
            else:
                screen.blit(player_body_image,(snake_pos[i][0],snake_pos[i][1]))           
        
    def att_snake():

        for i in range(len(snake_pos)-1,0,-1):
            snake_pos[i] = (snake_pos[i-1][0],snake_pos[i-1][1])

    def add_snake():
        snake_pos.append([0,0])

    #function to generate food
    def generate_food():
        global food_x
        global food_y
        food_x = random.randint(0,750)
        food_y = random.randint(0,550)
        screen.blit(food_image, (food_x, food_y))
    
    def show_food():
        global food_x
        global food_y
        screen.blit(food_image, (food_x, food_y))

    #function for movement  
    def player_movement(key_event, variation_x, variation_y, len_snake):
        
        if key_event.type == pygame.KEYDOWN:
            if key_event.key == pygame.K_LEFT:
                if variation_x == SNAKE_SIZE and len_snake >1:
                    return [variation_x, variation_y]
                else:
                    variation_x = -SNAKE_SIZE
                    return [variation_x, 0]
            if key_event.key == pygame.K_RIGHT: 
                if variation_x == -SNAKE_SIZE and len_snake >1:
                    return [variation_x, variation_y]
                else:
                    variation_x = SNAKE_SIZE 
                    return [variation_x, 0]
            if key_event.key == pygame.K_UP: 
                if variation_y == SNAKE_SIZE and len_snake >1:
                    return [variation_x, variation_y]
                else:
                    variation_y = -SNAKE_SIZE 
                    return [0, variation_y]
            if key_event.key == pygame.K_DOWN:
                if variation_y == -SNAKE_SIZE and len_snake >1:
                    return [variation_x, variation_y]
                else:
                    variation_y = SNAKE_SIZE 
                    return [0, variation_y]
        else:
            return [variation_x, variation_y]
              
    def check_snake_collision(snake_list):
        if len(snake_list)>1:
            for i in range(len(snake_list)-1, 0,-1):
                if snake_list[i] == snake_list[0]:
                    return True
        return False
            


    def check_position(update_x, update_y):
        if update_x >= 800-32 or update_x < 0:
            return False
        if update_y >= 800-32 or update_y < 0:
            return False
        else:
            return True

    #Calculate distance

    def check_collision_food(x_snake,y_snake, x_food, y_food):
        distance = math.sqrt((x_snake-x_food)**2 + (y_food-y_snake)**2)
        if distance <=27:
            return True
        else:
            
            return False
    
    def reset():
        global snake_pos
        snake_pos = [(SNAKE_INITIAL_X,SNAKE_INITIAL_Y)]




    def fail_grid():
        screen.fill((255,255,255))
        fail = failfont.render('You Failed', False, (0, 0, 0)) 
        textsurface = myfont.render('Score: ' + str(score), False, (0, 0, 0))
        screen.blit(textsurface,(300,250))       
        screen.blit(fail,(300,200))
        pygame.display.update()
                

    generate_food() 
    # main loop
    while running:
        # event handling, gets all event from the event queue
        if flag_fail == True:
            fail_grid()
        
        else:

            screen.fill((255,255,255))
            clock.tick(10)
            if check_collision_food(snake_pos[0][0],snake_pos[0][1],food_x, food_y) is False:            
                show_food()            
            else:
                generate_food()
                add_snake()
                score += 1
            if check_snake_collision(snake_pos):
                flag_fail = True

            if check_position(snake_pos[0][0] + player_variation[0], snake_pos[0][1] + player_variation[1]) == True:
                att_snake()
                snake_pos[0] = (snake_pos[0][0]+ player_variation[0], snake_pos[0][1]+ player_variation[1])
                player()
            else:
                flag_fail = True

            if check_snake_collision(snake_pos):
                flag_fail = True
            
            textsurface = myfont.render('Score: ' + str(score), False, (0, 0, 0))
            screen.blit(textsurface,(720,0))
            pygame.display.update()
            
            
        for event in pygame.event.get():
                #print(player_movement(event, player_variation[0], player_variation[1], len(snake_pos)))
                
            player_variation = player_movement(event, player_variation[0], player_variation[1], len(snake_pos))
            if flag_fail == True:
                if event.type == pygame.KEYDOWN:
                    print("Teste")
                    flag_fail = False
                    snake_pos = [(SNAKE_INITIAL_X,SNAKE_INITIAL_Y)] 
                    player_variation = [0,0]
                    generate_food()

                # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()