from Ax12 import Ax12
import time

# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
if __name__ == "__main__": 
    Ax12.DEVICENAME = '/dev/ttyUSB0'
    # Ax12.DEVICENAME = '/dev/ttyUSB1'

    Ax12.BAUDRATE = 1_000_000
    Ax12.DEBUG = True
    # sets baudrate and opens com port
    Ax12.connect()

    # create AX12 instance with ID 10 
    motor_id = 1
    my_dxl = Ax12(motor_id)  
    my_dxl.set_moving_speed(200)
    my_dxl.print_status

# def user_input():
#     """Check to see if user wants to continue"""
#     ans = input('Continue? : y/n ')
#     if ans == 'n':
#         return False
#     else:
#         return True


def motor_move(motor_object,gole_position):
    """ sets goal position based on user input """
    # while 1:
        # gole_position = int(input("goal pos: "))
    motor_object.set_goal_position(gole_position)
    time.sleep(0.7)        
    print(motor_object.get_present_position())
        


if __name__ == "__main__":
    # pass in AX12 object
    motor_move(my_dxl,0)

    # disconnect
    my_dxl.set_torque_enable(0)
    Ax12.disconnect()