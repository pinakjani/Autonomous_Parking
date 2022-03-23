from numpy import angle
import pygame
from env import draw_path, drawGrid, generate_obstacles, compute_obsmap
from env import Player
from Astar import Astar
import matplotlib.pyplot as plt

pygame.init()


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WHITE = (255,255,255)
BLACK = (0,0,0)

# Fill the background with white
screen = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])

player = Player((80,40))

field = drawGrid(WINDOW_WIDTH,WINDOW_HEIGHT,screen)
obs_map = compute_obsmap(field)

start = (6,2)
goal = (13,21)

path = Astar(obs_map,start,goal)
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
          
        # Check for QUIT event. If QUIT, then set running to false.
        
            print(player.angle)
        
    if count%100==0:
        player.i+=1

    generate_obstacles(screen)
    

    draw_path(screen,path)
    player.navigate(path)
    # for pos in path:
    #     sim_pos = ((pos[0]*20),(pos[1]*20))
    screen.blit(player.new_image,player.rect)
    # Flip the display
    pygame.display.flip()


print(path)

x = []
y = []
for (i,j) in path:
    x.append(i)
    y.append(j)
y.reverse()
x.reverse()
plt.plot(x,y)

plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
 
# giving a title to my graph
plt.title('Differential Drive Path')
plt.show()

# Done! Time to quit.
pygame.quit()