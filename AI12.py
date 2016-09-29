from __future__ import print_function
from collections import deque
from operator import attrgetter
from heapq import heappush
from heapq import heappop
from collections import defaultdict
import collections


class Point:
    def __init__(self, row, column, value): #***************
        self.col = column
        self.row = row
        self.val = value 
        self.parent = (-1,-1)
        self.heur = -1
        self.cost = 0
        self.func = self.heur + self.cost
    #def value_return(Point)
    def update_val(self,value):
        self.val=value
        #return Point.val
        #self.distance = distance
        #self.visited = 0
        #self.parent = parent


def make_maze(f): 
    row = 0
    maze=[]
    start=(0,0)
    end = []
    for line in f:
        array=[]
        col=0
        for char in line:
            if char != '\n':
                if char=='P':
                    start=(row,col)
                elif char=='.':
                    end.append((row,col))
                new_point=Point(row,col,char)
                array.append(new_point)
                col+=1
        maze.append(array)
        row+=1
    return maze, start, end


def print_maze(maze): 
    for y in range (0,len(maze)):
        for x in range (0,len(maze[0])):
            print(maze[y][x].val,end="")
        print("\n")
    

def near_point(maze, node):
    row_num=node.row
    col_num=node.col
    near_vals=[]
    if(maze[row_num][col_num+1].val!='%'):
        near_vals.append(maze[row_num][col_num+1])
    if(maze[row_num-1][col_num].val!='%'):
        near_vals.append(maze[row_num-1][col_num])
    if(maze[row_num][col_num-1].val!='%'):
        near_vals.append(maze[row_num][col_num-1])
    if(maze[row_num+1][col_num].val!='%'):
        near_vals.append(maze[row_num+1][col_num])
    return near_vals


# Recursive function to save the path, going from the goal to the start
# Pass in node = end node, path_cost = 0
# Everything is (y, x) here        
def store_path(maze, node, path_cost, start, path):
    if (node.row, node.col) != (start[0],start[1]):
        path_cost += 1
        path.append((node.row, node.col))
        store_path(maze, node.parent, path_cost, start, path)
    else:
        print('Path Cost =', path_cost)


# Calculates heuristic values for each node that is not a wall
# The Point.heur value is the Manhattan distance
def calculate_heuristics(maze, end_pt_cur):
    for y in range (0, len(maze)):
        for x in range (0, len(maze[0])):
            if maze[y][x].val != '%':
                maze[y][x].heur = abs(y - end_pt_cur[0]) + abs(x - end_pt_cur[1])
                maze[y][x].func = maze[y][x].cost + maze[y][x].heur


def distance_set(maze,end_pt,start_pt):
    dist=[]
    for one in end_pt:
        dist.append(abs(start_pt[0] - one[0]) + abs(start_pt[1] - one[1]))
    heap = []
    dict=defaultdict(list)
    n=0
    for one in dist:
        heappush(heap,one)
        dict[one].append(end_pt[n])
        n+=1
    od=collections.OrderedDict(sorted(dict.items()))
    return od, heap


# A* search function modified
def astar(maze, visited, expanded, start, end, value_i):
    node = maze[start[0]][start[1]]
    node.func = node.cost + node.heur
    heap = []
    heappush(heap, node.func)
    dict = defaultdict(list)
    dict[node.func].append(node)
    visited.append(node)

    path = []

    while heap:
        node = dict[heappop(heap)].pop()
        expanded.append(node)

        if node.val == '.':
            node.val = value_i
            #print('Node val, row, col:', node.val, node.row, node.col)
            store_path(maze, node, 0, start, path)
            break

        neighbors = near_point(maze, node)
        neighbors = sorted(neighbors, key=attrgetter('func'))

        for n in neighbors:
            if n.val == '%':
                continue
            elif n not in visited:
                visited.append(n)
                n.parent = node
                n.cost = node.cost + 1
                n.func = n.cost + n.heur
                heappush(heap, n.func)
                dict[n.func].append(n)

                #print('child', n.row, n.col, 'parent', node.row, node.col)
            else:
                i = visited.index(n)
                if (node.cost + 1 < visited[i].cost):
                    visited[i] = n

                    if n in dict[n.func]:
                        heap.remove(n.func)
                        dict[n.func].remove(n)

                        n.parent = node
                        n.cost = node.cost + 1
                        n.func = n.cost + n.heur

                        heappush(heap, n.func)
                        dict[n.func].append(n)

                        #print('child', n.row, n.col, 'parent', node.row, node.col)
                    else:
                        n.parent = node
                        n.cost = node.cost + 1
                        n.func = n.cost + n.heur

                        heappush(heap, n.func)
                        dict[n.func].append(n)

                        #print('child', n.row, n.col, 'parent', node.row, node.col)

    print('Number Of Expanded Nodes =', len(expanded))
    #print('Visited:')
    #for v in visited:
    #    print(v.row, v.col)
    #print('Path:', path)
    print('\n')          
    return (node.row,node.col)        


# A* search function with multiple dots
def astar2(maze, start_pt, end_pt):
    start = start_pt
    i = 0

    values = [0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','M']

    while end_pt:
        visited = []
        expanded = []

        od, heap = distance_set(maze, end_pt, start)
        end = od[heappop(heap)].pop()
        calculate_heuristics(maze, end)

        print('Start', start, 'End', end)

        node=astar(maze, visited, expanded, start, end, values[i])
        start=node
        end_pt.remove(node)
        #start = end
        i += 1

    #maze[start[0]][start[1]].val='A'


################################# Script Code ##################################

start_pt=(0,0)
end_pt = []
while True:
    name = input("Please select maze file for A* search on multiple dots:\n"
                "1: Tiny Search\n"
                "2: Small Search\n"
                "3: Medium Search\n"
                "4: Exit\n"
                "Your Choice:")
    if name == 4:
        sys.exit()
    elif name == 1:
        filename=open('tinySearch.txt','r')
    elif name == 2:
        filename=open('smallSearch.txt','r')
    elif name == 3:
        filename=open('mediumSearch.txt','r')
    else:
        print("Invalid Input")
        sys.exit()
    maze, start_pt, end_pt=make_maze(filename)
    print_maze(maze)
    start_row,start_col = start_pt
    astar2(maze, start_pt, end_pt)
    print_maze(maze)



print('Number of expanded nodes =', len(expanded))


file = 'mediumMaze.txt'
filename=open(file, 'r')
maze, start_pt, end_pt = make_maze(filename)

print_maze(maze)

start_row,start_col = start_pt

#calculate_heuristics(maze, start_pt)

astar2(maze, start_pt, end_pt)

print_maze(maze)
