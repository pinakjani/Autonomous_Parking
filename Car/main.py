import numpy as np
import pygame
from env import draw_path, drawGrid, generate_obstacles, compute_obsmap
from env import Player
from algorithm import Astar
from global_vars import*
import math
import matplotlib.pyplot as plt

pygame.init()



# Fill the background with white
screen = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
# field = np.zeros((WINDOW_WIDTH//blockSize,WINDOW_HEIGHT//blockSize))
player = Player((80,40))

field = drawGrid(WINDOW_WIDTH,WINDOW_HEIGHT,screen)
obs_map = compute_obsmap(field)

start = (6*2,2*2,0)
goal = (15*2,21*2,0)
goal1 = (13*2,21*2,0)
goal2 = (15*2,21*2,0)


path = Astar(obs_map,start,goal)
path.reverse()


path1 = Astar(obs_map,(15*2,21*2,0.272977),goal1)
path1.reverse()

path2 = Astar(obs_map,(13*2,21*2,0.14497),goal2)
path2.reverse()


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
        
    if count%70==0:
        player.i+=1

    generate_obstacles(screen)
    
    draw_path(screen,path)
    draw_path(screen,path1)
    draw_path(screen,path2)
    if player.i<60:
        player.navigate(path,player.i)
    elif player.i>=60 and player.i<65:
        player.navigate(path1,(player.i-60))
    else:
        # print("look",player.i)
        player.navigate(path2,(player.i-65))


    screen.blit(player.new_image,player.rect)
    # Flip the display
    pygame.display.flip()

# print(path)
# print(path1)
# print(path2)

x = []
y = []
for (i,j,k) in path:
    x.append(i)
    y.append(j)
for (i,j,k) in path1:
    x.append(i)
    y.append(j)
for (i,j,k) in path2:
    x.append(i)
    y.append(j)

y.reverse()
x.reverse()

# Done! Time to quit.
pygame.quit()

plt.plot(x,y)

plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
 
# giving a title to my graph
plt.title('Ackerman Drive Path')
plt.show()