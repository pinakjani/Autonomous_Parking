import numpy as np
import math
import pygame
from pygame import K_RETURN, K_RIGHT, K_LEFT, K_UP, K_DOWN, KEYUP
from pygame.math import Vector2
from global_vars import*


def drawGrid(WINDOW_WIDTH,WINDOW_HEIGHT,screen):
    #Set the size of the grid block
    field = np.zeros((WINDOW_WIDTH//blockSize,WINDOW_HEIGHT//blockSize))
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, BLACK, rect,1)
    return field

def draw_path(screen,path):
    for (i,j,k) in path:
        rect = pygame.Rect(i*blockSize, j*blockSize, blockSize, blockSize)
        pygame.draw.rect(screen, GREEN, rect)



def generate_obstacles(screen):
    pygame.draw.rect(screen,(0,0,0),pygame.Rect(300,120,160,140))
    # pygame.draw.rect(screen,(255,0,0),pygame.Rect(20,400,140,60))
    pygame.draw.rect(screen,(255,0,0),pygame.Rect(400,400,140,60))

def compute_obsmap(field):
    obs1x,obs1y = 300//blockSize,120//blockSize
    # obs2x,obs2y = 20//blockSize,400//blockSize
    obs3x,obs3y = 400//blockSize,400//blockSize
    for i in range(obs1x,obs1x+(160//blockSize)+1):
        for j in range(obs1y,obs1y+(140//blockSize)+1):
            field[i][j] = 1
    # for i in range(obs2x,obs2x+(140//blockSize)+1):
    #     for j in range(obs2y,obs2y+(60//blockSize)+1):
    #         field[i][j] = 1
    for i in range(obs3x,obs3x+(140//blockSize)+1):
        for j in range(obs3y,obs3y+(60//blockSize)+1):
            field[i][j] = 1
    return field



class Player:
    def __init__(self,pos=(260,40)):
        super(Player, self).__init__()
        self.surf = pygame.Surface((120, 60))
        self.trail1 = pygame.Surface((80, 60))
        # self.trail2 = pygame.Surface((80, 60))
        self.surf.fill(BLUE)
        self.trail1.fill(BLUE)
        # self.trail2.fill(BLUE)
        self.trail1.set_colorkey(BLACK)  
        self.trail1_copy = self.trail1.copy()
        # self.trail2.set_colorkey(BLACK)  
        # self.trail2_copy = self.trail2.copy()
        self.surf.set_colorkey(BLACK)  
        self.image = self.surf.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.surf, RED, (self.rect.midright),4)
        self.new_image = self.surf.copy()
        self.rect.center = pos
        self.trail1_rect = self.trail1_copy.get_rect()
        # self.trail2_rect = self.trail2.get_rect()
        self.trail1_rect.center = (80,40)
        # self.trail2_rect.center = (150,40)
        self.position = Vector2(pos)
        self.direction = Vector2(1, 0)  # A unit vector pointing rightward.
        self.speed = 0.01
        self.angle_speed = 0
        self.angle = 0
        self.i = 1
    
    def update(self):
        if self.angle_speed != 0:
            # Rotate the direction vector and then the image.
            # old_cent = self.rect.center
            self.direction.rotate_ip(self.angle_speed)
            self.angle = (self.angle+self.angle_speed)%360
            self.new_image = pygame.transform.rotate(self.surf, -self.angle)
            self.rect = self.new_image.get_rect()
            # self.rect.center = old_cent

        # Update the position vector and the rect.
        self.position += self.direction * self.speed
        self.rect.center = self.position
        
        if self.rect.left <= 0:
            self.speed = 0
        if self.rect.right >= WINDOW_WIDTH:
            self.speed = 0
        if self.rect.top <= 0:
            self.speed = 0
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.speed = 0
    
    def follow_path(self,path):
        i = 5
        # while(i<len(path)):
        k1,k2 = 0.011,0.01
        dist_error = math.sqrt(pow((path[i][1]-self.position[1]),2)+pow((path[i][0]-self.position[0]),2))
        m1,m2 = (self.direction[1]/self.direction[0]),(path[i][1]-self.position[1])/(path[i][0]-self.position[0])
        ang_error = math.atan2((m2-m1),(1-(m1*m2)))
        ang_error = math.degrees(ang_error)
        print("look",ang_error,dist_error)
        while (dist_error>0.4) or (ang_error>0.4):
            print(i,ang_error,dist_error)
            self.angle_speed = k1*ang_error
            self.speed = k2*dist_error
            self.direction.rotate_ip(self.angle_speed)
            self.angle = (self.angle+self.angle_speed)%360
            self.new_image = pygame.transform.rotate(self.surf, -self.angle)
            self.rect = self.new_image.get_rect()
                # self.rect.center = old_cent
            # Update the position vector and the rect.
            self.position += self.direction * self.speed
            self.rect.center = self.position
            dist_error = math.sqrt(pow((path[i][1]-self.position[1]),2)+pow((path[i][0]-self.position[0]),2))
            m1,m2 = (self.direction[1]/self.direction[0]),(path[i][1]-self.position[1])/(path[i][0]-self.position[0])
            ang_error = math.atan2((m2-m1),(1-(m1*m2)))
            ang_error = math.degrees(ang_error)
            # if dist_error<0.3 and ang_error<0.3:
            #     pass
            
            # i+=1
            # break
    def navigate(self,path,t1_dict,t):
        if t<len(path):
            ind = t
            # m = (path[ind][1]-path[ind-1][1])/(path[ind][0]-path[ind-1][0])
            # if ind == len(path)-1:
            #     ang = 0
            # else:
            # print("dekh",t1_dict[(path[ind][0],path[ind][1])][0])
            t1x,t1y,trail1_ang = t1_dict[(path[ind][0],path[ind][1])][0]
            # t2x,t2y,trail2_ang = t2_dict[(path[ind][0],path[ind][1])][0]
            ang = round(path[ind][2],2)
            # print("ang",ang)
            trail1_ang = round((trail1_ang*180/math.pi))
            # trail2_ang = round((trail2_ang*180/math.pi))
            self.angle = round((ang*180/math.pi))
            # print(path[ind][2],self.angle)
            self.new_image = pygame.transform.rotate(self.surf, -self.angle)
            self.trail1_copy = pygame.transform.rotate(self.trail1, -trail1_ang)
            # self.trail2_copy = pygame.transform.rotate(self.trail2, -trail2_ang)
            self.rect = self.new_image.get_rect()
            self.rect.centerx = (path[ind][0]*blockSize)
            self.rect.centery = (path[ind][1]*blockSize)
            self.trail1_rect = self.trail1_copy.get_rect()
            self.trail1_rect.centerx = round(t1x*blockSize)
            self.trail1_rect.centery = round(t1y*blockSize)
            # self.trail2_rect = self.trail2_copy.get_rect()
            # self.trail2_rect.centerx = (t2x*blockSize)
            # self.trail2_rect.centery = (t2y*blockSize)
    
def trailer_path(dict1,path):
    t1_path = []
    # t2_path = []
    for p in path:
        t1_path.append(dict1[(int(p[0]),int(p[1]))][0])
        # t2_path.append(dict2[(int(p[0]),int(p[1]))][0])
    return t1_path


       