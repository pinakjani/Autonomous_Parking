import numpy as np
import math
from global_vars import*
from collections import deque
import heapq


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
                
def heuristic3(node,goal):
    # Compute Eucledian Distance
    print("hey",goal[2],node[2])
    h3 = ((goal[2]-node[2]))*1
    print("hi",h3)
    return h3

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
                h2[rr][rc] += 2
                continue
            elif i==2 or i==-2 or j==2 or j==-2:
                h2[rr][rc] += 5
                continue
            else:
                h2[rr][rc] += 10
    return h2


def dijkstra_path(prev,goal,start):
    i,j,k = int(goal[0]),int(goal[1]),goal[2]
    path = []
    path.append((i,j,prev[i][j][2]))
    while(True):
        # print("jo",prev[i][j][2])
        path.append((prev[i][j][0],prev[i][j][1],prev[i][j][2]))
        # print("look",(prev[i][j][0],prev[i][j][1],prev[i][j][2]))
        if prev[i][j][0]==start[0] and prev[i][j][1]==start[1] and prev[i][j][2]==start[2]:
            break
        # else:
        #     print("nonono")
        m,n = int(i),int(j)
        i = int(prev[m][n][0])
        j = int(prev[m][n][1])
        
    return path

def Astar(field,start,goal):
    cost = np.ones((grid_width,grid_height))*float('inf')
    h2 = heuristic2(field)
    visited = np.zeros((grid_width,grid_height))
    u_s_val = [1.5, 0, -1.5]
    u_phi_val = [math.pi/9, 0, -math.pi/9]
    L = 2
    prev = np.full((128,128,3),(0.0,0.0,0.0))
    path = deque()
    cost[start[0]][start[1]] = 0
    pq = [(0,(start[0],start[1]),start[2])]
    count = 0
    while len(pq)>0:
        cost_list = []
        curr_distance,curr_node,curr_head = heapq.heappop(pq)
        visited[curr_node[0]][curr_node[1]] = 1
        if curr_node[0] == goal[0] and curr_node[1] ==goal[1] and curr_head==goal[2]:
            path = dijkstra_path(prev,goal,start)
            return path
        for u_s in u_s_val:
            for u_phi in u_phi_val:
                theta_next = (u_s * math.tan(u_phi) / L) + curr_head
                rr = round((u_s * math.cos(theta_next)) + curr_node[0])
                rc = round((u_s * math.sin(theta_next)) + curr_node[1])
                position = rr, rc
                heading = theta_next
                if rr<0 or rc<0:
                    continue
                elif rr>=grid_width or rc>=grid_height:
                    continue
                elif field[rr][rc] == 1:
                    continue
                elif (u_s<0):
                    new_cost = cost[curr_node[0]][curr_node[1]]+12+heuristic1((rr,rc),goal)+h2[rr][rc]
                else:   
                    new_cost = cost[curr_node[0]][curr_node[1]]+10+heuristic1((rr,rc),goal)+h2[rr][rc] 
                if new_cost<cost[rr][rc]:
                    cost[rr][rc] = new_cost
                    # print("look",curr_node[0],curr_node[1],curr_head)
                    cost_list.append((new_cost,position,heading))
        if len(cost_list)>0:
            min_cost_node = min(cost_list, key = lambda t: t[0])
            print("wow",min_cost_node)
            heapq.heappush(pq,min_cost_node)
            prev[min_cost_node[1][0]][min_cost_node[1][1]] = [curr_node[0],curr_node[1],curr_head]
    print("out",cost)
    path = dijkstra_path(prev,goal,start)
    return path


