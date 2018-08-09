from robot import *
import time
import random


print ("Modules imported")
Speeds=[0.0,0.25,0.5,0.75,1,0.75,0.5,0.25,0.0,-0.25,-0.5,-0.75,-1,-0.75,-0.5,-0.25]

cfactor_l = 1
cfactor_r = 1
speed_l = 0
speed_r = 0
r = Robot()
servo_board = r.servo_board

print ("Variables set")


def set_speed(r, speed, wheel = 2):
    global cfactor_l
    global cfactor_r
    if wheel == 0:
       r.motor_board.m0 = speed*cfactor_l
       print ("Left wheel speed override.")
    if wheel == 1:
       r.motor_board.m1 = speed*cfactor_r
       print ("Right wheel speed override.")
    if wheel == 2:
       r.motor_board.m0 = speed*cfactor_l
       r.motor_board.m1 = speed*cfactor_r
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
    global cfactor_l
    global cfactor_r

    speeds_list = [speed_l, speed_r, speed_l]
    if stop>speeds_list[wheel]:
        if wheel == 0:
            while speed_l<stop:
                speed_l = round((speed_l + interval), 2)
                r.motor_board.m0 = speed_l*cfactor_l
                time.sleep(delay)
            print("Left wheel speed set to "+str(speed_l*100)+"%")
        elif wheel == 1:
            while speed_r<stop:
                speed_r = round((speed_r + interval), 2)
                r.motor_board.m1 = speed_r*cfactor_r
                time.sleep(delay)
            print("Right wheel speed set to "+str(speed_r*100)+"%")

        elif wheel == 2:
            straighten(r)
            while speed_l<stop:
                speed_l = round((speed_l + interval), 2)
                speed_r = speed_l
                r.motor_board.m0 = speed_l*cfactor_l
                r.motor_board.m1 = speed_l*cfactor_r
                time.sleep(delay)
            print("Left wheel speed set to "+str(speed_l*100)+"%")
            print("Right wheel speed set to "+str(speed_r*100)+"%")
    if stop<speeds_list[wheel]:
        if wheel == 0:
            while speed_l>stop:
                speed_l = round((speed_l - interval), 2)
                r.motor_board.m0 = speed_l*cfactor_l
                time.sleep(delay)
            print("Left wheel speed set to "+str(speed_l*100)+"%")
        elif wheel == 1:
            while speed_r>stop:
                speed_r = round((speed_r - interval), 2)
                r.motor_board.m1 = speed_r*cfactor_r
                time.sleep(delay)
            print("Right wheel speed set to "+str(speed_r*100)+"%")

        elif wheel == 2:
            straighten(r)
            while speed_l>stop:
                speed_l = round((speed_l - interval), 2)
                speed_r = speed_l
                r.motor_board.m0 = speed_l*cfactor_l
                r.motor_board.m1 = speed_l*cfactor_r
                time.sleep(delay)
            print("Left wheel speed set to "+str(speed_l*100)+"%")
            print("Right wheel speed set to "+str(speed_r*100)+"%")
        

        
def straighten(r, mode = 1):
    """Stops a turn"""
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
          return servo_board.read_ultrasound(6,7)
    elif sensor == 2:
          return servo_board.read_ultrasound(8,9)
    elif sensor == 3:
          return servo_board.read_ultrasound(10,11)


def turn2(r, direction):
    """Turns the robot
    :param direction: "l" for left, "r" for right
    """
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
    """Moves the robot away from the edge"""
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
    """Main running function"""
    set_speed(r, 0.2, wheel = 2)
    print("Main program initialised.")
    
    df = read_ultrasound(1)    
    dr = read_ultrasound(2)
    dl = read_ultrasound(3)
    print (df)
    print (dr)
    print (dl)
    print ("")
    print ("Ultrasound testing complete. Starting program.")
    

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
    """Gets the can"""
    accel(r, wheel = 2, stop = 0.5)
    time.sleep(5)
    #r.grab() ##breaks front ultrasound sensor.
     
          

def test(r):
    """Tests robot"""
    
    global speed_r
    global speed_l
    print ("Accelerating.")
    accel(r, wheel = 2, stop = 1, interval = 0.01, delay = 0.01)
    time.sleep(1)
    print ("Braking.")
    accel(r, wheel = 2, stop = 0, interval = 0.01)
    time.sleep(5)
    print ("Top speed maintain.")
    accel(r, wheel = 2, stop = 1)
    time.sleep(5)
    print ("Smooth tranisition to reverse.")
    accel(r, wheel = 2, stop = -1, interval = 0.01, delay = 0.01)
    time.sleep(3)
    accel(r, wheel = 2, stop = 1, interval = 0.01, delay = 0.01)
    print ("Turn left.")
    accel(r, wheel = 0, stop = 0.1*speed_r, delay = 0.01)
    time.sleep(2)
    accel(r, wheel = 2, stop = 1, interval = 0.01, delay = 0.01)
    print ("Turn right.")
    accel(r, wheel = 1, stop = 0.1*speed_l, delay = 0.01)
    accel(r, wheel = 2, stop = 1, interval = 0.01, delay = 0.01)
    time.sleep(2)
    accel(r, wheel = 2, stop = 0, interval = 0.01)
    time.sleep(2)
    print ("Spin clockwise.")
    accel(r, wheel = 0, stop = 1, delay = 0.01)
    accel(r, wheel = 1, stop = -1, delay = 0.01)
    time.sleep(5)
    accel(r, wheel = 2, stop = 0, interval = 0.01)
    time.sleep(5)
    print ("Spin anticlockwise.")
    accel(r, wheel = 1, stop = 1, delay = 0.01)
    accel(r, wheel = 0, stop = -1, delay = 0.01)
    time.sleep(5)
    accel(r, wheel = 2, stop = 0, interval = 0.01)
    time.sleep(5)
    print ("Reading sensors.")
    df = read_ultrasound(1)
    dr = read_ultrasound(2)
    dl = read_ultrasound(3)
    print ("Distance forward = "+str(df)+" metres.")
    print ("Distance left = "+str(dl)+" metres.")
    print ("Distance right = "+str(dr)+" metres.")
    
    
def calibrate(r):
    global speed_r
    global speed_l
    print ("Left wheel testing.")
    for i in range (2):
        accel(r, wheel = 0, stop = 1)
        time.sleep(40)
        accel(r, wheel = 0, stop = 0)
        time.sleep(10)
#    for speed in range (5, 100, 5):
#        set_speed(r, (speed/100), wheel = 0)
#        time.sleep(20)
#    print ("Right wheel testing.")
#    accel(r, wheel = 1, stop = 1)
#    time.sleep(40)
#    accel(r, wheel = 1, stop = 0)

#    for speed in range (5, 100, 5):
#        set_speed(r, (speed/100), wheel = 1)
#        time.sleep(20)
    
        
def random_bot(r):
    while True:
        df = read_ultrasound(1)
        thing = random.randint(1, 3)
#        if df<0.2 and df != 0:
#            print ("Stuck...")
#            print ("Reversing.")
#            accel(r, wheel = 2, stop = -1, delay = 0.01)
#            time.sleep(0.5)
#            accel(r, wheel = 2, stop = -0.1, delay = 0.01)

        if thing == 1:
            speed = random.uniform(0, 1)
            wheel = random.randint(0, 2)
            accel(r, wheel = wheel, stop = speed, delay = 0.001)
        elif thing == 2:
            speed_l = random.uniform(0, -1)
            speed_r = random.uniform(0, 1)
            accel(r, wheel = 0, stop = speed_l, delay = 0.001)
            accel(r, wheel = 1, stop = speed_r, delay = 0.001)
        elif thing == 3:
            speed_r = random.uniform(0, -1)
            speed_l = random.uniform(0, 1)
            accel(r, wheel = 0, stop = speed_l, delay = 0.001)
            accel(r, wheel = 1, stop = speed_r, delay = 0.001)
        time.sleep(random.uniform(0, 2))



        
print ("Functions set")   


get_can(r)
print("Main program starting. ")
go2(r)
#test(r)
#calibrate(r)
#random_bot(r)
