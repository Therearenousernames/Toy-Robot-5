import turtle

paths = []
obs_list = []
# create maze
def get_obstacles():
    global paths
    """Generates the obstacles and the paths.
    Returns:
        tuples: a tuple containing a list of 
                obstacles and a list of paths.
    """         
    maze1 = '''################# #######################
# #   #     #     #   #   #       # #   #
# ### # # # # ### # # # ### # # # # # ###
# #   # # #   #   # #     # # # #     # #
# # # ####### # ####### ####### ##### # #
#   #             # #     #     #   #   #
# ##### ### ### # # ### # # ##### ### ###
#     # # # #   #   # # #     # # #     #
### ##### # ##### ### ### # ### # # #####
        # #   #     #     # # #   # #   
# # # ### # # #####     # # # # ##### ###
# # # #     # #         # #     # #     #
# ### # # ######### ### ####### # ##### #
# #   # # #   # #     #   # # # #   # # #
# ### ####### # ### # ##### # # ### # # #
#   #         # #   # # #     #       # #
##### # ### ### ### ### # # # # # # # # #
#     # #   #     #   #   # #   # # #   #
# # # # ### # ### ### ### # ### ### ### #
# # # #   #   #   #   #   #   #   #   # #
################### #####################'''.strip().split('\n')

    for i in maze1:
        print(i)
    obstacles = []
    start_y = (20*len(maze1))//2
    start_x = -(20*len(maze1[0]))//2
    print(start_x,start_y)
    for i in maze1:
       for x in i:
           if x in [' ']:
               paths.append((start_x,start_y))
           elif x in ['-','+','|','#']:
                obstacles.append((start_x,start_y))
                obs_list.append((start_x,start_y))
           start_x+= 20
       
       start_x = -(20*len(maze1[0]))//2
       start_y -= 20

    return obstacles

    


def square_obstacles(obstacles):
    """Generates the representation of a square obstacle.
    Args:
        cords (list): a list of coordinates which are stored in
                        tuples of (x, y)
    Returns:
        list : a list of lists that represent a square obstacle 
                generated from a given sequence.
    """    
    if len(obstacles) == 0:
        return []
    else:
        square = []
        for i in obstacles:
            x,y = i[0],i[1]
            square.append([(x,y), (x+20,y), (x+20,y+20), (x,y+20), (x,y)])
        return square


def draw_obstacles(t,obstacles):
    # t.shapesize(0.4)
    t.penup()
    t.speed(0)
    turtle.tracer(0)
    t.shape('square')

    for obs in obstacles:
        x,y = obs[0][0],obs[0][1]
        t.pencolor('green')
        t.fillcolor('black')
        t.goto(x+10,y-10)
        t.pendown()
        t.stamp()
        t.penup()

    turtle.tracer(1)
    t.shape('classic')
    t.color('red')
    t.goto(0,0)


def is_position_blocked(x1, y1, cords):
    """This function checks if the x and y coordinates are 
    within an obstacle.
    Args:
        x1 (integer): x coordinate
        y1 (integer): y coordinate
        cords (list): a list of coordinates which are store 
                        in tuples of (x, y)
    Returns:
        bool: a bool value of True or False that indicates
                 whether the x and y coordinates are in a 
                 obstacle
    """    
    for x,y in cords: 
        if x1 in range(x, x+21) and y1 in range(y-21,y):
            return True
    return False


def is_path_blocked(x1,y1,x2,y2, cords):
    """This function checks the path between two (x,y) 
    coordinates and returns a True or False if there 
    is an obstacle in between the (x1,y1) and (x2,y2).
    Args:
        x1 (integer): x coordinate 
        y1 (integer): y coordinate
        x2 (integer): x cooordinate
        y2 (integer): y coordinate
        cords (list): a list of coordinates which are store 
                        in tuples of (x, y)
    Returns:
        boolean: a bool value of True or False that indicates
                 whether it's possible for the robot to move 
                 from (x1,y1) to (x2,y2) - if there is no 
                 obstacle between the two coordinates.
    """    
    x,y = x1,y1
    difference_y, difference_x= (y2-y1), (x2-x1)
    if difference_y > 0 or difference_x> 0:
        increment = 1
    else:
        increment = -1 
    if x1 == x2:
        for _ in range(abs(difference_y)):
            y += increment
            if is_position_blocked(x1, y, cords) == True:
                return True
    elif y1 == y2:
        for _ in range(abs(difference_x)):
            x += increment
            if is_position_blocked(x, y1, cords) == True:
                return True
    return False


def printing_obstacles(robot_name,cords):
    """Prints the obstacles.
    Args:
        cords (list): a list of randomly generated coords.
    """    
    if cords != []:
        print(f'{robot_name}: Loaded obstacles.')
        print('There are some obstacles:')
        for x,y in cords:
            print(f'- At position {x},{y} (to {x+20},{y-20})')




