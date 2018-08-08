from robot import *
from math import pi
import time

r = Robot()

motor_board = r.motor_board

motor_board.m0 = 1
motor_board.m1 = 1

time.sleep(3)

motor_board.m1 = 0

time.sleep(3)

motor_board.m1 = 1

print('done')
