import turtle
# from robot import maze


maze = False
# variables tracking position and direction
position_x = 0
position_y = 0
directions = ['forward', 'right', 'back', 'left']
current_direction_index = 0
new_x, new_y = 0, 0

# area limit vars
min_y, max_y = -210, 210
min_x, max_x = -410, 410

def creating_a_screen():
    """This function creates an instance of the
    the screen.
    Returns:
        instance: a screen
    """   
    window = turtle.Screen()
    window.title('Toy Robot 4')
    window.screensize(500, 500)
    return window


def make_turtle():
    """This function creates an instance of 
    the turtle
    Returns:
        turtle: an instance of a turtle
    """   
    bot = turtle.Turtle()
    bot.color('green')
    bot.pen(speed=1)
    return bot


def make_boundary(bot):
    """This function draws the boundary.
    Args:
        bot (turtle): an instance of a turtle
                        that draws the boundary
    """    
    bot.penup()
    bot.rt(90)
    bot.goto(-410, 210)
    bot.pendown()
    bot.pencolor('red')
    for i in range(2):
        bot.forward(820)
        bot.right(90)
        bot.forward(420)
        bot.right(90)
    bot.pencolor('green')
    bot.penup()
    bot.goto(0, 0)
    bot.left(90)
    


def show_position(robot_name):
    """This function moves the robot to the intended 
    coordinates.
    """    
    robot.goto(position_x, position_y)
    print(f'> {robot_name} now at position ({position_x},{position_y})' )


def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """
    return min_x <= new_x <= max_x and min_y <= new_y <= max_y



robot = make_turtle()
window = creating_a_screen()


