from robot import *
import time
print ("Modules imported")
Speeds=[0.0,0.25,0.5,0.75,1,0.75,0.5,0.25,0.0,-0.25,-0.5,-0.75,-1,-0.75,-0.5,-0.25]


speed_l = 0
speed_r = 0
r = Robot()
print ("Variables set")


def set_speed(r, speed, wheel = 2):
    if wheel == 0:
       r.motor_board.m0 = speed
       print ("Left wheel speed override.")
    if wheel == 1:
       r.motor_board.m1 = speed
       print ("Right wheel speed override.")
    if wheel == 2:
       r.motor_board.m0 = speed
       r.motor_board.m1 = speed
       print ("Speed override.")

def accel(r, wheel=2, stop=1, interval=0.05, delay=0.05):
    """
    :param r: robot object
    :param wheel: 0 for left, 1 for right, 2 for both
    :param stop: desired final speed
    :param interval: jumps in speed
    :param delay: delay between speed jumps
    """
    
    global speed_l
    global speed_r

    speeds_list = [speed_l, speed_r, speed_l]
    if stop>speeds_list[wheel]:
        if wheel == 0:
            while speed_l<stop:
                speed_l = round((speed_l + interval), 2)
                r.motor_board.m0 = speed_l
                time.sleep(delay)
            print("Left wheel speed set to "+str(speed_l*100)+"%")
        elif wheel == 1:
            while speed_r<stop:
                speed_r = round((speed_r + interval), 2)
                r.motor_board.m1 = speed_r
                time.sleep(delay)
            print("Right wheel speed set to "+str(speed_r*100)+"%")

        elif wheel == 2:
            straighten(r)
            while speed_l<stop:
                speed_l = round((speed_l + interval), 2)
                speed_r = speed_l
                r.motor_board.m0 = speed_l
                r.motor_board.m1 = speed_l
                time.sleep(delay)
            print("Left wheel speed set to "+str(speed_l*100)+"%")
            print("Right wheel speed set to "+str(speed_r*100)+"%")
    if stop<speeds_list[wheel]:
        if wheel == 0:
            while speed_l>stop:
                speed_l = round((speed_l - interval), 2)
                r.motor_board.m0 = speed_l
                time.sleep(delay)
            print("Left wheel speed set to "+str(speed_l*100)+"%")
        elif wheel == 1:
            while speed_r>stop:
                speed_r = round((speed_r - interval), 2)
                r.motor_board.m1 = speed_r
                time.sleep(delay)
            print("Right wheel speed set to "+str(speed_r*100)+"%")

        elif wheel == 2:
            straighten(r)
            while speed_l>stop:
                speed_l = round((speed_l - interval), 2)
                speed_r = speed_l
                r.motor_board.m0 = speed_l
                r.motor_board.m1 = speed_l
                time.sleep(delay)
            print("Left wheel speed set to "+str(speed_l*100)+"%")
            print("Right wheel speed set to "+str(speed_r*100)+"%")
        

        
def straighten(r, mode = 1):
    global speed_l
    global speed_r


    if mode == 1:
        if speed_l>speed_r:
            print ("Straightening")
            accel(r, wheel = 1, stop = speed_l, delay = 0.01)
        else:
            print ("Straightening")
            accel(r, wheel = 0, stop = speed_r, delay = 0.01)

            
def read_ultrasound(sensor):
    """
    :param sensor: 1 = forward, 2 = right, 3 = left

    """
    if sensor == 1:
          return r.servo_board.read_ultrasound(6,7)
    if sensor == 2:
          return r.servo_board.read_ultrasound(8,9)
    if sensor == 3:
          return r.servo_board.read_ultrasound(10,11)


def turn2(r, direction):
    global speed_r
    global speed_l
    dr = read_ultrasound(2)
    dl = read_ultrasound(3)
    if direction == "l":
        accel(r, wheel = 0, stop = 0.1*speed_r, delay = 0.001)
        while True:
            temp = read_ultrasound(2)
            if temp < dl:
                dl = temp
                continue
            else:
                accel(r, wheel = 0, stop = speed_r, delay = 0.001)
                break
    if direction == "r":
        accel(r, wheel = 1, stop = 0.1*speed_l, delay = 0.001)
        while True:
            temp = read_ultrasound(3)
            if temp < dr:
                dr = temp
                continue
            else:
                accel(r, wheel = 1, stop = speed_l, delay = 0.001)
                break
            
    

def middle(r):
    dr = read_ultrasound(2)
    dl = read_ultrasound(3)
    if dr<0.2:
        print("Too close to edge, correcting.")        
        while dr<=0.3:
            accel(r, wheel = 0, stop = 0.7, delay = 0.001)
            dr = read_ultrasound(2)
        while dr<0.4:
            accel(r, wheel = 0, stop = 1, delay = 0.001)
            accel(r, wheel = 1, stop = 0.7, delay = 0.001)
            dr = read_ultrasound(2)
        accel(r, wheel = 1, stop = 1, delay = 0.001)
    elif dl<0.2:
        print("Too close to edge, correcting.")
        while dl<=0.3:
            accel(r, wheel = 1, stop = 0.7, delay = 0.001)
            dl = read_ultrasound(3)
        while dl<0.4:
            accel(r, wheel = 1, stop = 1, delay = 0.001)
            accel(r, wheel = 0, stop = 0.7  , delay = 0.001)
            dl = read_ultrasound(3)
        accel(r, wheel = 0, stop = 1, delay = 0.001)

            
def go2(r):
    set_speed(r, 0.2, wheel = 2)
    while True:
        df = read_ultrasound(1)
        dr = read_ultrasound(2)
        dl = read_ultrasound(3)
        if df<0.2 and df != 0:
            print ("Stuck...")
            print ("Reversing.")
            accel(r, wheel = 2, stop = -1, delay = 0.01)
            time.sleep(0.7)
            accel(r, wheel = 2, stop = 0.75, delay = 0.01)
        #print(distance_f)
#        if dr<0.5 or dl<0.5:
#            middle(r)

        elif df > 1.5:
            accel(r, stop = 1)
            #time.sleep(5)
            
        elif df<=1.5:
            if dr != 0 and dl != 0:
                if dl<dr:
                    print ("Turning right.")
                    turn2(r, "r")
                else:
                    print ("Turning left.")
                    turn2(r, "l")
                
            
def get_can(r):
    accel(r, wheel = 2, stop = 0.5)
    time.sleep(5)

print ("Functions set")        
          






get_can(r)
go2(r)
