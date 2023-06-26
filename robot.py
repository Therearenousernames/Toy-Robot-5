import sys
import random
from mazerunner import *

obs = []
is_obs = False

maze = False
turtle = False

if 'maze' in sys.argv:
    import maze.the_worlds_most_confusing_maze as obstacles
    maze = True
else:
    import  maze.obstacles as obstacles


if 'turtle' in sys.argv:
    from world.turtle import world
    from world.turtle.world import robot
    turtle = True
else:
    from world.text import world


# list of valid command names
valid_commands = ['off', 'help', 'replay', 'forward', 'back', 'right', 'left', 'sprint','mazerun']
move_commands = valid_commands[3:]

#commands history
history = []

def get_robot_name():
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    return name


def get_command(robot_name):
    """
    Asks the user for a command, and validate it as well
    Only return a valid command
    """

    prompt = ''+robot_name+': What must I do next? '
    command = input(prompt)
    while len(command) == 0 or not valid_command(command):
        output(robot_name, "Sorry, I did not understand '"+command+"'.")
        command = input(prompt)

    return command.lower()


def split_command_input(command):
    """
    Splits the string at the first space character, to get the actual command, as well as the argument(s) for the command
    :return: (command, argument)
    """
    args = command.split(' ', 1)
    if len(args) > 1:
        return args[0], args[1]
    return args[0], ''


def is_int(value):
    """
    Tests if the string value is an int or not
    :param value: a string value to test
    :return: True if it is an int
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def valid_command(command):
    """
    Returns a boolean indicating if the robot can understand the command or not
    Also checks if there is an argument to the command, and if it a valid int
    """
    (command_name, arg1) = split_command_input(command)
    if command_name == 'mazerun' and arg1 in ['top','left','right','bottom','']:
        return True
    if command_name in  ['forward', 'back', 'sprint'] and arg1 == '':
        return False
    elif command_name in ['forward', 'back', 'sprint'] and is_int(arg1) == True:
        return True

    elif command_name.lower() == 'replay':
        if len(arg1.strip()) == 0:
            return True
        elif (arg1.lower().find('silent') > -1 or arg1.lower().find('reversed') > -1)\
        and len(arg1.lower().replace('silent', '').replace('reversed','').strip()) == 0:
            return True
        else:
            range_args = arg1.replace('silent', '').replace('reversed','')
            if is_int(range_args):
                return True
            else:
                range_args = range_args.split('-')
                return is_int(range_args[0]) and is_int(range_args[1]) and len(range_args) == 2
    else:
        return command_name.lower() in valid_commands and (len(arg1) == 0 or is_int(arg1))


def output(name, message):
    print(''+name+": "+message)
    

def do_help():
    """
    Provides help information to the user
    :return: (True, help text) to indicate robot can continue after this command was handled
    """
    return True, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
REPLAY - replays all movement commands from history [FORWARD, BACK, RIGHT, LEFT, SPRINT]
"""


def do_forward(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    global world,is_obs
    if update_position(steps):
        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.'
    if is_obs == True:
        is_obs = False
        return True, f'{robot_name}: Sorry, there is an obstacle in the way.'   
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_back(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    global world,is_obs
    if update_position(-steps):
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.'
    if is_obs == True:
        is_obs = False
        return True, f'{robot_name}: Sorry, there is an obstacle in the way.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_right_turn(robot_name):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """
    global world
    
    world.current_direction_index
    world.current_direction_index += 1
    if world.current_direction_index > 3:
        world.current_direction_index = 0
    if turtle == True:
        world.robot.rt(90)
    return True, ' > '+robot_name+' turned right.'


def do_left_turn(robot_name):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """
    global world
    world.current_direction_index

    world.current_direction_index -= 1
    if world.current_direction_index < 0:
        world.current_direction_index = 3
    if turtle == True:
        world.robot.lt(90)

    return True, ' > '+robot_name+' turned left.'


def do_sprint(robot_name, steps):
    """
    Sprints the robot, i.e. let it go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    :param robot_name:
    :param steps:
    :return: (True, forward output)
    """

    if steps == 1:
        return do_forward(robot_name, 1)
    else:
        (do_next, command_output) = do_forward(robot_name, steps)
        print(command_output)
        return do_sprint(robot_name, steps - 1)


def get_commands_history(reverse, relativeStart, relativeEnd):
    """
    Retrieve the commands from history list, already breaking them up into (command_name, arguments) tuples
    :param reverse: if True, then reverse the list
    :param relativeStart: the start index relative to the end position of command, e.g. -5 means from index len(commands)-5; None means from beginning
    :param relativeEnd: the start index relative to the end position of command, e.g. -1 means from index len(commands)-1; None means to the end
    :return: return list of (command_name, arguments) tuples
    """

    commands_to_replay = [(name, args) for (name, args) in list(map(lambda command: split_command_input(command), history)) if name in move_commands]
    if reverse:
        commands_to_replay.reverse()

    range_start = len(commands_to_replay) + relativeStart if (relativeStart is not None and (len(commands_to_replay) + relativeStart) >= 0) else 0
    range_end = len(commands_to_replay) + relativeEnd if  (relativeEnd is not None and (len(commands_to_replay) + relativeEnd) >= 0 and relativeEnd > relativeStart) else len(commands_to_replay)
    return commands_to_replay[range_start:range_end]


def do_replay(robot_name, arguments):
    """
    Replays historic commands
    :param robot_name:
    :param arguments a string containing arguments for the replay command
    :return: True, output string
    """

    silent = arguments.lower().find('silent') > -1
    reverse = arguments.lower().find('reversed') > -1
    range_args = arguments.lower().replace('silent', '').replace('reversed', '')

    range_start = None
    range_end = None

    if len(range_args.strip()) > 0:
        if is_int(range_args):
            range_start = -int(range_args)
        else:
            range_args = range_args.split('-')
            range_start = -int(range_args[0])
            range_end = -int(range_args[1])

    commands_to_replay = get_commands_history(reverse, range_start, range_end)

    for (command_name, command_arg) in commands_to_replay:
        (do_next, command_output) = call_command(command_name, command_arg, robot_name)
        if not silent:
            print(command_output)
            world.show_position(robot_name)

    return True, ' > '+robot_name+' replayed ' + str(len(commands_to_replay)) + ' commands' + (' in reverse' if reverse else '') + (' silently.' if silent else '.')


def call_command(command_name, command_arg, robot_name):
    if command_name == 'help':
        return do_help()
    elif command_name == 'forward':
        return do_forward(robot_name, int(command_arg))
    elif command_name == 'back':
        return do_back(robot_name, int(command_arg))
    elif command_name == 'right':
        return do_right_turn(robot_name)
    elif command_name == 'left':
        return do_left_turn(robot_name)
    elif command_name == 'sprint':
        return do_sprint(robot_name, int(command_arg))
    elif command_name == 'replay':
        return do_replay(robot_name, command_arg)
    elif command_name == 'mazerun':
        if maze:
            return mazerun(robot_name, command_arg)
        return mazerun_obs(robot_name,command_arg)
    return True,''


def mazerun_obs(robot_name,arg):
    print('starting maze run..')
    while True:
        if arg in ['','top']:
            if world.position_x in range(world.min_x,world.max_x) and world.position_y == world.max_y:
                return True,'I am at the top edge'
            elif world.current_direction_index == 0:
                old_x,old_y = world.position_x,world.position_y
                handle_command(robot_name,'forward 5')
                new_x,new_y = world.position_x,world.position_y
                if (old_x,old_y) == (new_x,new_y):
                    handle_command(robot_name,random.choice(['left','right']))
                    handle_command(robot_name,'forward 10')
            else:
                handle_command(robot_name,random.choice(['left','right']))
        if arg in ['bottom']:
            if world.position_x in range(world.min_x,world.max_x) and world.position_y == world.min_y:
                return True,'I am at the bottom edge'
            elif world.current_direction_index == 2:
                old_x,old_y = world.position_x,world.position_y
                handle_command(robot_name,'forward 5')
                new_x,new_y = world.position_x,world.position_y
                if (old_x,old_y) == (new_x,new_y):
                    handle_command(robot_name,random.choice(['left','right']))
                    handle_command(robot_name,'forward 10')
            else:
                handle_command(robot_name,random.choice(['left','right']))
        if arg in ['right']:
            if world.position_x == world.max_x and world.position_y in range(world.min_y,world.max_y):
                return True,'I am at the right edge'
            elif world.current_direction_index == 1:
                old_x,old_y = world.position_x,world.position_y
                handle_command(robot_name,'forward 5')
                new_x,new_y = world.position_x,world.position_y
                if (old_x,old_y) == (new_x,new_y):
                    handle_command(robot_name,random.choice(['left','right']))
                    handle_command(robot_name,'forward 10')
            else:
                handle_command(robot_name,random.choice(['left','right']))
        if arg in ['left']:
            if world.position_x == world.min_x and world.position_y in range(world.min_y,world.max_y):
                return True,'I am at the left edge'
            elif world.current_direction_index == 3:
                old_x,old_y = world.position_x,world.position_y
                handle_command(robot_name,'forward 5')
                new_x,new_y = world.position_x,world.position_y
                if (old_x,old_y) == (new_x,new_y):
                    handle_command(robot_name,random.choice(['left','right']))
                    handle_command(robot_name,'forward 10')
            else:
                handle_command(robot_name,random.choice(['left','right']))

def mazerun(robot_name,command_arg):
    print('starting maze run..')
    # robot current position
    robot_x,robot_y = world.position_x, world.position_y
    
    # list of paths
    paths = obstacles.paths
    
    # robot starting cell
    initial_cell = converting_initial_position_to_inital_cell(robot_x,robot_y, paths)
    
    # distance from robot_current_position to the center of it's cell
    dy = initial_cell[1]-10 - world.position_y
    
    # move to the center
    handle_command(robot_name,f'forward {dy}')
    
    # get the end_cell that the robot should move to
    if command_arg in ['', 'top']:
        end = paths[0]
    if command_arg in ['bottom']:
        end = paths[-1]
    if command_arg in ['right']:
        end = paths[196]
    if command_arg in ['left']:
        end = paths[166]
    
    # get all the neighbours related to the starting position using bfs
    solution = search(initial_cell,paths)
    
    # get the path to follow using backtracking
    road = backtracking(initial_cell, end, solution)
    
    #count initialization
    count = 0 
    while count < len(road)-1:
        # robots current direction
        current_direction =  world.current_direction_index
        
        difx,dify = 20,20
        # finds the cell above, below, right and left
        top_n = (road[count][0], road[count][1]+20)
        bottom_n =(road[count][0], road[count][1]-20)
        left_n = (road[count][0]-20, road[count][1])
        right_n = (road[count][0]+20, road[count][1])

        if current_direction == 0:
            if road[count+1] == top_n:
                handle_command(robot_name,f'forward {abs(dify)}')
            elif road[count+1] == bottom_n:
                handle_command(robot_name, f'right')
                handle_command(robot_name, f'right')
                handle_command(robot_name,f'forward {abs(dify)}')
            elif road[count+1] == left_n:
                handle_command(robot_name,f'left')
                handle_command(robot_name,f'forward {abs(difx)}')
            elif road[count+1] == right_n:
                handle_command(robot_name,f'right')
                handle_command(robot_name,f'forward {abs(difx)}')
        elif current_direction == 1:
            if road[count+1] == top_n:
                handle_command(robot_name,f'left')
                handle_command(robot_name,f'forward {abs(difx)}')
            elif road[count+1] == bottom_n:
                handle_command(robot_name,f'right')
                handle_command(robot_name,f'forward {abs(difx)}')
            elif road[count+1] == left_n:
                handle_command(robot_name, f'right')
                handle_command(robot_name, f'right')
                handle_command(robot_name,f'forward {abs(dify)}')
            elif road[count+1] == right_n:
                handle_command(robot_name,f'forward {abs(dify)}')
        elif current_direction == 2:
            if road[count+1] == top_n:
                handle_command(robot_name, f'right')
                handle_command(robot_name, f'right')
                handle_command(robot_name,f'forward {abs(dify)}')
            elif road[count+1] == bottom_n:
                handle_command(robot_name,f'forward {abs(dify)}')
            elif road[count+1] == left_n:
                handle_command(robot_name,f'right')
                handle_command(robot_name,f'forward {abs(difx)}')
            elif road[count+1] == right_n:
                handle_command(robot_name,f'left')
                handle_command(robot_name,f'forward {abs(difx)}')
        elif current_direction == 3:
            if road[count+1] == top_n:
                handle_command(robot_name,f'right')
                handle_command(robot_name,f'forward {abs(difx)}')
            elif road[count+1] == bottom_n:
                handle_command(robot_name,f'left')
                handle_command(robot_name,f'forward {abs(difx)}')
            elif road[count+1] == left_n:
                handle_command(robot_name,f'forward {abs(dify)}')
            elif road[count+1] == right_n:
                handle_command(robot_name, f'right')
                handle_command(robot_name, f'right')
                handle_command(robot_name,f'forward {abs(dify)}')
        count+=1
    # return statements after the robot get's to the edge
    if command_arg in ['','top']:
        return True,'I am at the top edge'
    elif command_arg in ['bottom']:
        return True, 'I am at the bottom edge'
    elif command_arg in ['left']:
        return True,'I am the left edge'
    elif command_arg in ['right']:
        return True, 'I am at the right edge'
    return True, ""


def update_position(steps):
    """
    Update the current x and y positions given the current direction, and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """

    global world
    new_x = world.position_x
    new_y = world.position_y

    if world.directions[world.current_direction_index] == 'forward':
        new_y = new_y + steps
    elif world.directions[world.current_direction_index] == 'right':
        new_x = new_x + steps
    elif world.directions[world.current_direction_index] == 'back':
        new_y = new_y - steps
    elif world.directions[world.current_direction_index] == 'left':
        new_x = new_x - steps
    
    if obstacles.is_path_blocked(world.position_x, world.position_y, new_x, new_y, obs):
        global is_obs
        is_obs = True
    if world.is_position_allowed(new_x, new_y) and not obstacles.is_path_blocked(world.position_x, world.position_y, new_x, new_y, obs):
        world.position_x = new_x
        world.position_y = new_y
        return True
    
    return False

                        


def handle_command(robot_name, command):
    """
    Handles a command by asking different functions to handle each command.
    :param robot_name: the name given to robot
    :param command: the command entered by user
    :return: `True` if the robot must continue after the command, or else `False` if robot must shutdown
    """

    (command_name, arg) = split_command_input(command)

    if command_name == 'off':
        return False
    else:
        (do_next, command_output) = call_command(command_name, arg, robot_name)
    print(command_output)
    world.show_position(robot_name)
    add_to_history(command)
    return do_next


def add_to_history(command):
    """
    Adds the command to the history list of commands
    :param command:
    :return:
    """
    history.append(command)
    return history


def robot_start():
    """This is the entry point for starting my robot"""
    global history,world,obstacles,obs
    robot_name = get_robot_name()
    output(robot_name, "Hello kiddo!")
    

    obs = obstacles.get_obstacles()
    world.obs = obs
    obstacles.printing_obstacles(robot_name,obs)
    if turtle == True:
        robot.lt(90)
        square = obstacles.square_obstacles(obs)
        obstacles.draw_obstacles(robot, square)
        if maze == False:
            world.make_boundary(robot)
        else:
            obstacles.maze = True
    world.position_x = 0
    world.position_y = 0
    world.current_direction_index = 0
    history = []
    command = get_command(robot_name)
    while handle_command(robot_name, command):
        command = get_command(robot_name)
    output(robot_name, "Shutting down..")



if __name__ == "__main__":
    robot_start()
