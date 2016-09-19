
filename = 'mediumMaze.txt'

maze = []
row = 0
start = (0,0)
end = (0,0)

with open(filename, 'r') as f:
    for line in f:
        array = []
        col = 0

        for char in line:
            if char != '\n':
                array.append(char)
                if char == 'P':
                    start = (row, col)
                elif char == '.':
                    end = (row, col)
            col += 1
    
        maze.append(array)
        row += 1

length = len(maze)
height = len(maze[0])


root = Point(start[0], start[1], maze[start[1]][start[0]], distance, NULL)
near_vals = near_point(root)


