from matplotlib.pyplot import grid
import numpy as np
import math
from collections import deque
import heapq

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

grid_width = WINDOW_WIDTH//20
grid_height = WINDOW_HEIGHT//20


def heuristic1(node,goal):
    # Compute Eucledian Distance
    # print(goal,node)
    h =pow((goal[1]-node[1]),2)+pow((goal[0]-node[0]),2)
    # print(h)
    return math.sqrt(h)

def heuristic2(field):
    h2 = field*100
    for i in range(field.shape[0]):
        for j in range(field.shape[1]):
            if field[i][j]==1:
                h2 = potfield(h2,i,j)
    return h2
                


def potfield(h2,x,y):
    di = [1,0,-1,2,-2,3,-3]
    dj = [1,0,-1,2,-2,3,-3]
    for i in di:
        for j in dj:
            rr = x+i
            rc = y+j
            if rr<0 or rc<0:
                continue
            elif rr>=grid_width or rc>=grid_height:
                continue
            elif i==0 and j==0:
                continue
            elif i==3 or i==-3 or j==-3 or j==3:
                h2[rr][rc] += 15
                continue
            elif i==2 or i==-2 or j==2 or j==-2:
                h2[rr][rc] += 25
                continue
            else:
                h2[rr][rc] += 50
    return h2


def dijkstra_path(prev,goal,start):
    i,j = goal[0],goal[1]
    path = []
    path.append((i,j))
    while(True):
        path.append((prev[i][j][0],prev[i][j][1]))
        if prev[i][j][0]==start[0] and prev[i][j][1]==start[1]:
            break
        m,n = i,j
        i = prev[m][n][0]
        j = prev[m][n][1]
        
    return path

def Astar(field,start,goal):
    cost = np.ones((grid_width,grid_height))*float('inf')
    h2 = heuristic2(field)
    visited = np.zeros((grid_width,grid_height))
    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
    prev = np.full((128,128,2),(0,0))
    path = deque()
    cost[start[0]][start[1]] = 0
    pq = [(0,(start[0],start[1]))]
    count = 0
    while len(pq)>0:
        curr_distance,curr_node = heapq.heappop(pq)
        visited[curr_node[0]][curr_node[1]] = 1
        if curr_node[0] == goal[0] and curr_node[1] ==goal[1]:
            path = dijkstra_path(prev,goal,start)
            return path
        for (x,y) in neighbors:
            rr,rc = curr_node[0]+x,curr_node[1]+y
            if rr<0 or rc<0:
                continue
            elif rr>=grid_width or rc>=grid_height:
                continue
            elif visited[rr][rc] == 1 or field[rr][rc] == 1:
                continue
            elif (x==1 or x==-1) and (y==1 and y==-1):
                new_cost = cost[curr_node[0]][curr_node[1]]+14+heuristic1((rr,rc),goal)+h2[rr][rc]
            else:   
                new_cost = cost[curr_node[0]][curr_node[1]]+10+heuristic1((rr,rc),goal)+h2[rr][rc] 
            if new_cost<cost[rr][rc]:
                cost[rr][rc] = new_cost
                prev[rr][rc] = [curr_node[0],curr_node[1]]
                heapq.heappush(pq,(new_cost,(rr,rc)))
    path = dijkstra_path(prev,goal,start)
    return path
