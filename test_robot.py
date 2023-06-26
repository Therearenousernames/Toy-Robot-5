import sys
from robot import *
import unittest
from io import StringIO
from unittest.mock import patch


history.clear()

class TestingRobot(unittest.TestCase):
    sys.stdout = StringIO()
    @patch('sys.stdin', StringIO('Spock\nC3P0\nIronMan'))
    def testing_get_robot_name(self):
        self.assertEqual(get_robot_name(), 'Spock')
        self.assertEqual(get_robot_name(), 'C3P0')
        self.assertEqual(get_robot_name(), 'IronMan')
    

    @patch('sys.stdin', StringIO('\nHal'))
    def testing_get_robot_name_empty_string_and_valid_input(self):
        self.assertEqual(get_robot_name(), 'Hal')


    @patch('sys.stdin', StringIO(' \nRIGHT'))
    def testing_get_command_empty_string(self):
        name = 'HAL'
        self.assertEqual(get_command(name), 'right')

    
    @patch('sys.stdin', StringIO('fast\nforward 10'))
    def testing_get_command_invalid_command(self):
        name = 'HAL'
        self.assertEqual(get_command(name), 'forward 10')


    @patch('sys.stdin', StringIO('back 10'))
    def testing_get_command_valid_command_back(self):
        name = 'HAL'
        self.assertEqual(get_command(name), 'back 10')


    @patch('sys.stdin', StringIO('left'))
    def testing_get_command_valid_command_left(self):
        name = 'Spock'
        self.assertEqual(get_command(name), 'left')
    

    def testing_split_command_input_two_args(self):
        self.assertEqual(split_command_input('forward 10'), ('forward', '10'))

    
    def testing_split_command_input_one_arg(self):
        self.assertEqual(split_command_input('right'), ('right', ''))


    def testing_is_int_invalid(self):
        self.assertEqual(is_int('#'), False)
        self.assertEqual(is_int(''), False)


    def testing_is_int_integer(self):
        self.assertTrue(is_int('5'), True)


    def testing_valid_command_valid(self):
        self.assertEqual(valid_command('forward 10'), True)
        self.assertEqual(valid_command('replay silent reversed'), True)
        self.assertEqual(valid_command('replay reversed 1'), True)

    def testing_valid_command_invalid_arg_two(self):
        self.assertEqual(valid_command('forward'), False)


    def testing_do_help(self):
        self.assertEqual(do_help(),(True, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
REPLAY - replays all movement commands from history [FORWARD, BACK, RIGHT, LEFT, SPRINT]
""" ))


    def testing_do_forward(self):
        name = "Spock"
        self.assertEqual(do_forward(name, 10),(True, ' > Spock moved forward by 10 steps.'))

    
    def testing_do_back(self):
        name = 'Tshepiso'
        self.assertEqual(do_back(name, 40),(True, ' > Tshepiso moved back by 40 steps.')) 

    def testing_do_right(self):
        name = 'Spock'
        self.assertEqual(do_right_turn(name), (True, f' > {name} turned right.'))

    
    def testing_do_left(self):
        name = 'Spock'
        self.assertEqual(do_left_turn(name), (True, f' > {name} turned left.'))

    
    def testing_sprinting(self):
        name = 'Tshepiso'
        self.assertEqual(do_sprint(name, 1), (True, ' > Tshepiso moved forward by 1 steps.'))



    def testing_do_replay(self):
        name = 'Tshepiso'
        self.assertEqual(do_replay(name, 'silent'), (True, ' > Tshepiso replayed 1 commands silently.'))
        self.assertEqual(do_replay(name, 'reversed'), (True, ' > Tshepiso replayed 1 commands in reverse.'))


    def testing_add_to_history(self):
        self.assertEqual(add_to_history('right'), ['right'])
        


if __name__ == '__main__':
    unittest.main()