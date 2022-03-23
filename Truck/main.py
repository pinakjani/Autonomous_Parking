import numpy as np
import pygame
from env import draw_path, drawGrid, generate_obstacles, compute_obsmap, trailer_path
from env import Player
from algorithm import Astar
from global_vars import*
import math
import matplotlib.pyplot as plt


pygame.init()



# Fill the background with white
screen = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
# field = np.zeros((WINDOW_WIDTH//blockSize,WINDOW_HEIGHT//blockSize))
player = Player((260,70))

field = drawGrid(WINDOW_WIDTH,WINDOW_HEIGHT,screen)
obs_map = compute_obsmap(field)

start = (26,8,0)
# start = (20,6,0)
goal = (30,42,0)
# goal = (55,22,0)
# goal1 = (25,15,0)
goal1 = (26,42,0)
goal2 = (30,42,0)
# goal = (2,15,-math.pi/4)

path,dict1= Astar(obs_map,start,goal)
path.reverse()


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
          

        
    if count%100==0:
        player.i+=1

    generate_obstacles(screen)
    
    draw_path(screen,path)

    player.navigate(path,dict1,player.i)
    screen.blit(player.new_image,player.rect)
    screen.blit(player.trail1_copy,player.trail1_rect.center)
    # screen.blit(player.trail2_copy,player.trail2_rect.center)
    # Flip the display
    pygame.display.flip()

print(path)
t1= trailer_path(dict1,path)
# print(t1)
x = []
y = []
for (i,j,k) in path:
    x.append(i)
    y.append(j)
y.reverse()
x.reverse()
plt.plot(x,y)

plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
 
# giving a title to my graph
plt.title('Trailer Drive Path')
plt.show()

# Done! Time to quit.
pygame.quit()