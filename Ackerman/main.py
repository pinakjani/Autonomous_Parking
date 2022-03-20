from numpy import angle
import pygame
from env import draw_path, drawGrid, generate_obstacles, compute_obsmap
from env import Player
from algorithm import Astar
from global_vars import*
import math

pygame.init()



# Fill the background with white
screen = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])

player = Player((80,40))

field = drawGrid(WINDOW_WIDTH,WINDOW_HEIGHT,screen)
obs_map = compute_obsmap(field)

start = (6,2,0)
goal = (15,21,0)
# goal = (5,8,math.pi/2)
# goal1 = (25,15,0)
goal1 = (13,22,0)
goal2 = (15,21,0)
# goal = (2,15,-math.pi/4)

path = Astar(obs_map,start,goal)
path.reverse()


path1 = Astar(obs_map,(15,21,0.272977),goal1)
path1.reverse()

path2 = Astar(obs_map,(13,22,0.272977),goal2)
path2.reverse()

path3 = [(15.0, 21.0, 0.272977),(14,21,0.272977/2),(13,21,0)]

running = True
count=0

while running:
    count+=1    
    screen.fill(WHITE)
    field = drawGrid(WINDOW_WIDTH,WINDOW_HEIGHT,screen)
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == pygame.K_ESCAPE:
                running = False
          
        # Check for QUIT event. If QUIT, then set running to false.
        
            # print(player.angle)
        
    if count%100==0:
        player.i+=1
    # pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    # player.update()

    # pygame.draw.rect(screen,(0,255,0),pygame.Rect(20,20,140,60))
    generate_obstacles(screen)
    
    draw_path(screen,path)
    draw_path(screen,path3)
    if player.i<30:
        player.navigate(path,player.i)
    # elif player.i>35 and player.i<40:
    #     draw_path(screen,path1)
    #     player.navigate(path1,(player.i-35))
    else:
        
        player.navigate(path3,(player.i-30))

    # for pos in path:
    #     sim_pos = ((pos[0]*20),(pos[1]*20))
    # print("player.i",player.i)
    screen.blit(player.new_image,player.rect)
    # Flip the display
    pygame.display.flip()


print(path2)

# Done! Time to quit.
pygame.quit()