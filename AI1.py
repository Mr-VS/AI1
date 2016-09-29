from __future__ import print_function
from collections import deque
from operator import attrgetter
from heapq import heappush
from heapq import heappop
from collections import defaultdict
import sys


class Point:
    parent=None
    
    def __init__(self, row, column, value): #***************
        self.col = column
        self.row = row
        self.val = value 
        self.cost=0
        self.heur=0
        
    #def value_return(Point)
    def update_val(self,value):
        self.val=value
    def save_parent(self, node):
        self.parent=node
    def add_heur(self,heur):
        self.heur=heur
    def change_g(self,g):
        self.g=g
    def change_f(self):
        self.f=self.g+self.heur

        #return Point.val
        #self.distance = distance
        #self.visited = 0
        #self.parent = parent
    
def return_pt_val(cur_pt):
    return cur_pt.val
start_pt=(0,0)
end_pt=(0,0)
def make_maze(f): 
    global row
    global col
    row = 0
    maze=[]
    start=(0,0)
    end=(0,0)
    for line in f:
        #line=line.rstrip('\n')
        array=[]
        col=0
        for char in line:
            if char != '\n':
                if char=='P':
                    start=(row,col)
                elif char=='.':
                    end=(row,col)
                new_point=Point(row,col,char)
                array.append(new_point)
                col+=1
        maze.append(array)
        row+=1
    return maze, start, end

def print_maze(maze): 
    for x in range (0,len(maze)):
        for y in range (0,len(maze[0])):
            print(return_pt_val(maze[x][y]),end="")
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

# Recursive function to mark path with periods, going from the goal to the start
# Pass in node = end node, path_cost = 0             
def mark_path(maze, node, path_cost, start_pt):
    if (node.row, node.col) != (start_pt[0], start_pt[1]):
        path_cost += 1
        node.val = '.'
        mark_path(maze, node.parent, path_cost, start_pt)
    else:
        print('Path cost =', path_cost)

def bfs(maze, visited, start_pt):
    node = maze[start_pt[0]][start_pt[1]]
    queue = deque([node])
    visited.append(node)
    while queue:
        node = queue.popleft();
        expanded.append(node)

        if node.val == '.':
            mark_path(maze, node, 0, start_pt)
            break

        neighbors = near_point(maze, node)

        for n in neighbors:
            if n.val == '%':
                continue
            elif n not in visited:
                visited.append(n)
                n.parent = node
                queue.append(n)

def dfs(maze,visited,start_pt):
    visited.append(maze[start_pt[0]][start_pt[1]])
    stack = [maze[start_pt[0]][start_pt[1]]]
    while stack:
        vertex = stack.pop()
        if vertex.val == '.':
            mark_path(maze, vertex, 0, start_pt)
            break
        neighbour = near_point(maze, vertex)
        for one in neighbour:
            if one =='%':
                continue
            elif one not in visited:
                visited.append(one)
                one.parent = vertex
                stack.append(one)

# Greedy best-first search function
def greedy(maze, visited, start_pt):
    node = maze[start_pt[0]][start_pt[1]]
    heap = []
    heappush(heap, node.heur)
    dict = defaultdict(list)
    dict[node.heur].append(node)
    visited.append(node)

    while heap:
        node = dict[heappop(heap)].pop()
        expanded.append(node)

        if node.val == '.':
            mark_path(maze, node, 0, start_pt)
            break

        neighbors = near_point(maze, node)
        neighbors = sorted(neighbors, key=attrgetter('heur'))

        for n in neighbors:
            if n.val == '%':
                continue
            elif n not in visited:
                visited.append(n)
                n.parent = node
                n.cost = node.cost + 1
                heappush(heap, n.heur)
                dict[n.heur].append(n)
            else:
                i = visited.index(n)
                if (node.cost + 1 < visited[i].cost):
                    print('replace')
                    visited[i] = n

                    if n in dict[n.heur]:
                        j = dict[n.heur].index(n)
                        dict[n.heur][j] = n
                    else:
                        heappush(heap, n.heur)
                        dict[n.heur].append(n)

                    n.parent = node
                    n.cost = node.cost + 1

    print('Number of expanded nodes =', len(expanded))


# A* search function
def astar(maze, visited, start_pt):
    node = maze[start_pt[0]][start_pt[1]]
    node.func = node.cost + node.heur
    heap = []
    heappush(heap, node.func)
    dict = defaultdict(list)
    dict[node.func].append(node)
    visited.append(node)

    while heap:
        node = dict[heappop(heap)].pop()
        expanded.append(node)

        if node.val == '.':
            mark_path(maze, node, 0, start_pt)
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
            else:
                i = visited.index(n)
                if (node.cost + 1 < visited[i].cost):
                    print('replace')
                    visited[i] = n

                    if n in dict[n.func]:
                        heap.remove(n.func)
                        dict[n.func].remove(n)

                        n.parent = node
                        n.cost = node.cost + 1
                        n.func = n.cost + n.heur

                        heappush(heap, n.func)
                        dict[n.func].append(n)
                    else:
                        n.parent = node
                        n.cost = node.cost + 1
                        n.func = n.cost + n.heur

                        heappush(heap, n.func)
                        dict[n.func].append(n)

    print('Number of expanded nodes =', len(expanded))

# Calculates heuristic values for each node that is not a wall
# The Point.heur value is the Manhattan distance
def calculate_heuristics(maze, end_pt):
    for y in range (0, len(maze)):
        for x in range (0, len(maze[0])):
            if maze[y][x].val != '%':
                maze[y][x].heur = abs(y - end_pt[0]) + abs(x - end_pt[1])
                maze[y][x].func = maze[y][x].cost + maze[y][x].heur
                

while True:
    name = input("Please select maze file:\n"
                "1: Medaium Maze\n"
                "2: Big Maze\n"
                "3: Open Maze\n"
                "4: Exit\n"
                "Your Choice:")
    if name == 4:
        sys.exit()
    elif name == 1:
        filename=open('mediumMaze.txt','r')
    elif name == 2:
        filename=open('bigMaze.txt','r')
    elif name == 3:
        filename=open('openMaze.txt','r')
    else:
        print("Invalid Input")
        sys.exit()
    search_strat = input("Please choose search meathod:\n"
                    "1: DFS\n"
                    "2: BFS\n"
                    "3: Greedy best-first\n"
                    "4: A*\n"
                    "Your Choice:")
    maze, start_pt, end_pt=make_maze(filename)
    print_maze(maze)
    calculate_heuristics(maze,end_pt)
    visited = []
    expanded = []
    if search_strat == '1':
        dfs(maze,visited,start_pt)
    elif search_strat == 2:
        bfs(maze,visited,start_pt)
    elif search_strat == 2:
        greedy(maze,visited,start_pt)
    elif search_strat == 2:
        astar(maze,visited,start_pt)
    else:
        print("Invalid Input")
        sys.exit()
    print_maze(maze)
    print('Number of expanded nodes =', len(expanded))





#print(return_pt(maze[2][1]))

#print (maze)
#print (start_pt, end_pt)
start_row,start_col=start_pt
end_row,end_col=end_pt
#print (start_row,start_col)
#stack=[(maze[start_row][start_col].row,maze[start_row][start_col].col)]
#vertex=stack.pop()
#print (vertex)
#dfs(maze,visited,maze[start_row][start_col])
#bfs(maze,visited,start_pt)
#print_maze(maze)
#print ("Total node:"+str(len(visited)))
visited=[]
expanded=[]
bfs(maze,visited,start_pt)
#greedy(maze,visited,maze[start_row][start_col])
print_maze(maze)
print('Number of expanded nodes =', len(expanded))
#print('greedy cost = ', cost_greedy)









