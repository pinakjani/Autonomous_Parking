import numpy as np
import math
from global_vars import*
from collections import deque
import heapq


grid_width = WINDOW_WIDTH//blockSize
grid_height = WINDOW_HEIGHT//blockSize


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
                
def h3(node,goal):
    # Compute Eucledian Distance
    # print("hey",goal[2],node[2])
    t= node[2]
    # if node[2]>(math.pi/2):
        # t = node[2]-math.pi
    h = abs(goal[2]-t)
    # print("h3",h3)
    return h

def potfield(h2,x,y):
    di = [1,0,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7]
    dj = [1,0,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7]
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
            elif i==7 or i==-7 or j==-7 or j==7:
                h2[rr][rc] += 15
                continue
            elif i==6 or i==-6 or j==6 or j==-6:
                h2[rr][rc] += 20
                continue
            else:
                h2[rr][rc] += 25
    return h2




def dijkstra_path(prev,goal,start):
    i,j = int(goal[0]),int(goal[1])
    path = []
    path.append((i,j,prev[i][j][2]))
    count =1
    while(True):
        # print(prev[i][j][2])
        path.append((prev[i][j][0],prev[i][j][1],prev[i][j][2]))
        if prev[i][j][0]==start[0] and prev[i][j][1]==start[1] and prev[i][j][2]==start[2]:
            break
        # else:
        #     print("nonono")
        m,n = int(i),int(j)
        i = int(prev[m][n][0])
        j = int(prev[m][n][1])
        count+=1
    return path

def Astar(field,start,goal):
    cost = np.ones((grid_width,grid_height))*float('inf')
    h2 = heuristic2(field)
    visited = np.zeros((grid_width,grid_height))
    u_s_val = [2, 0, -2]
    u_phi_val = [math.pi/6,math.pi/9, -math.pi/9,-math.pi/6,0]
    L = 9
    d1 = 20
    d2 = 11
    dirn = 1
    prev = np.full((128,128,3),(0.0,0.0,0.0))
    trail1 = {}
    # trail2 = {}
    trail1[(start[0],start[1])] = [(start[0]-14,start[1],0)]
    # trail2[(start[0],start[1])] = [(15,4)]
    path = deque()
    cost[start[0]][start[1]] = 0
    pq = [(0,(start[0],start[1]),start[2],dirn,(start[0]-14,start[1],0))]
    reverse_cost = 300
    forward_cost = 10
    while len(pq)>0:
        cost_list = []
        k1 = 0
        k2 = 10
        k3 = 0 
        k4 = 1
        curr_distance,curr_node,curr_head,curr_dirn,curr_trail1 = heapq.heappop(pq)
        theta1 = curr_trail1[2]
        visited[curr_node[0]][curr_node[1]] = 1
        if curr_node[0] == goal[0] and curr_node[1] ==goal[1] and curr_head==goal[2]:
            path = dijkstra_path(prev,goal,start)
            return path
        # if curr_node[0] == goal[0] and curr_node[1] ==goal[1]:
            # goalt1,goalt2 = curr_trail1
            # start1,start2 = (4,4,0),(15,4,0)
        elif heuristic1((curr_node[0],curr_node[1],curr_head),goal)<20:
            reverse_cost = 5
            forward_cost = 5
            k1 = 0
            k2 = 0
            k3 = 200
        for u_s in u_s_val:
            for u_phi in u_phi_val:
                theta_next = round((u_s * round(math.tan(u_phi),3) / L),3) + curr_head
                rr = round((u_s * math.cos(theta_next)) + curr_node[0])
                rc = round((u_s * math.sin(theta_next)) + curr_node[1])
                trail1_theta_next = round(((u_s*math.sin(theta_next-theta1)/d1)+theta1),2)
                # trail2_theta_next = round(((u_s*math.cos(theta_next-theta1)*math.sin(theta1-theta2)/2*d2)+theta2),2)
                # trail1_x_next = round(u_s*math.cos(trail1_theta_next)+curr_trail1[0])
                # trail1_y_next = round(u_s*math.sin(trail1_theta_next)+curr_trail1[1])
                trail1_x_next = round(rr-(d1*math.cos(trail1_theta_next)))
                trail1_y_next = round(rc-(d1*math.sin(trail1_theta_next)))
                # trail2_x_next = round(u_s*math.cos(trail2_theta_next)+curr_trail2[0])
                # trail2_y_next = round(u_s*math.sin(trail2_theta_next)+curr_trail2[1])
                trail1_next = (trail1_x_next,trail1_y_next,trail1_theta_next)
                # trail2_next = (trail2_x_next,trail2_y_next,trail2_theta_next)
                position = rr, rc
                heading = theta_next
                # trailer = (trail1_theta_next,trail2_theta_next)
                # print("heading",theta_next)
                if rr<0 or rc<0 or trail1_x_next<0 or trail1_y_next<0:
                    continue
                elif rr>=grid_width or rc>=grid_height or trail1_x_next>grid_height or trail1_y_next>grid_width:
                    continue
                # elif field[trail1_x_next][trail1_y_next] == 1:
                #     continue
                elif (u_s<0):
                    new_dirn = -1
                    dirn_cost = abs(curr_dirn-(new_dirn))
                    # print("dirn_cost",dirn_cost)
                    new_cost = cost[curr_node[0]][curr_node[1]]+reverse_cost+(k2*dirn_cost)+(heuristic1((rr,rc),goal)*(1+k1*abs(u_phi)))+(h2[rr][rc])+(k3*h3((rr,rc,heading),goal))
                    # *(1+(9/math.pi)*abs(u_phi))
                else:   
                    new_dirn = 1
                    dirn_cost = abs(curr_dirn-(new_dirn))
                    # print("dirn_cost",dirn_cost)
                    new_cost = cost[curr_node[0]][curr_node[1]]+forward_cost+(k2*dirn_cost)+(heuristic1((rr,rc),goal)*(1+k1*abs(u_phi)))+(h2[rr][rc])+(k3*h3((rr,rc,heading),goal)) 
                    # *(1+(9/math.pi)*abs(u_phi))
                if (new_cost<cost[rr][rc]):
                    cost[rr][rc] = new_cost
                    # print("look",curr_node[0],curr_node[1],curr_head)
                    cost_list.append((new_cost,position,heading))
                    prev[rr][rc] = [curr_node[0],curr_node[1],curr_head]
                    trail1[(rr,rc)] = [trail1_next]
                    # trail2[(rr,rc)] = [trail2_next]
                    heapq.heappush(pq,(new_cost,position,heading,new_dirn,trail1_next))
        # print("dekh bc",cost_list)
    # print("out",field)
    path = dijkstra_path(prev,goal,start)
    return path,trail1


