import random

def  generate_number():
    return random.randint(0,10)

def get_obstacles():
    """Generate the obstacles between specified ranges which
    are the maximum values allowed for x and y respectively.
    Args:
        n (integer): the number of obstacles that will be 
                        generated.
    Returns:
        list: a list of coordinates which are stored in
                 tuples of (x, y).
    """ 
    number = random.randint(0, 10)
    cords = []
    for i in range(number):
        cords.append((random.randint(-100, 100), random.randint(-200, 200)))
    return cords


def square_obstacles(cords):
    """Generates the representation of a square obstacle.
    Args:
        cords (list): a list of coordinates which are stored in
                        tuples of (x, y)
    Returns:
        list : a list of lists that represent a square obstacle 
                generated from a given sequence.
    """    
    if len(cords) == 0:
        return []
    else:
        square = []
        for i in cords:
            x,y = i[0],i[1]
            square.append([(x,y), (x+4,y), (x+4,y+4), (x,y+4), (x,y)])
        return square


def draw_obstacles(t, square):
    """
    This function draws the generated square obstacles.
    Args:
        t (turtle): draws the obstacles.
        square (list): a list of lists that represents a square obstacles
                        generated from a given sequence.
    """    
    t.penup()
    for i in square:
        t.color('red', 'red')
        t.begin_fill()
        for j in i:
            x, y = j[0], j[1]
            t.goto(x,y)
            t.pendown()
        t.end_fill()
        t.penup()
    t.goto(0,0)
    t.color('green')


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
        if x1 in range(x, x+5) and y1 in range(y, y+5):
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
    if difference_y or difference_x> 0:
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
            print(f'- At position {x},{y} (to {x+4},{y+4})')
           



