#!/usr/bin/env python3
import time
import rclpy
from enum import Enum
from threading import Thread
from rclpy.node import Node
from rclpy.task import Future
from typing import NamedTuple
from geometry_msgs.msg import Twist
import axis_calibration as ac
import threading
import tkinter
import copy

from hiwin_interfaces.srv import RobotCommand
# from YoloDetector import YoloDetectorActionClient
DEFAULT_VELOCITY = 20
DEFAULT_ACCELERATION = 20

'''
    read axis
'''
tea_axis, puf_axis , egg_axis = [] , [] ,[]
axis = []
with open('src/competition/axis_calibration.txt') as A:
    for eachline in A:
        tmp = eachline.split()
        # print(tmp)
        axis.append(tmp)
     
tea_cali = list(map(float,axis[0]))
puf_cali = list(map(float,axis[1])) 
egg_cali = list(map(float,axis[2])) 

print(tea_cali)
print(puf_cali)
print(egg_cali)

standby_pass = [40.792, 153.685, 252.876, 158.365, 18.949, 1.696]
standby = [232.82, 260.402, 428.323, 158.364, 18.948, -8.696]

tea =   [
            [239.607+tea_cali[0], 365.833+tea_cali[1], 422.635, 158.364, 18.948, -8.696],
            [239.607+tea_cali[0], 365.833+tea_cali[1], 394.623+tea_cali[2], 158.364, 18.948, -8.696],
            [239.607+tea_cali[0], 196.554+tea_cali[1], 392.623+tea_cali[2], 158.364, 18.948, -8.696],
            [239.607+tea_cali[0], 381.157            , 394.623+tea_cali[2], 158.364, 18.948, -8.696],
            [239.607+tea_cali[0], 364.833+tea_cali[1], 394.623+tea_cali[2], 158.364, 18.948, -8.696],
            [239.607+tea_cali[0], 364.833+tea_cali[1], 422.635, 158.364, 18.948, -8.696]
        ]
tea_and_puf = [301.504, 335.833, 429.29, 158.369, 18.949, -8.714]

puf =   [#關到底
            [360.118+puf_cali[0], 366.628+puf_cali[1], 429.750, 158.368, 18.949, -8.713],
            [360.118+puf_cali[0], 366.628+puf_cali[1], 392.067+puf_cali[2], 158.368, 18.949, -8.713],
            [360.119+puf_cali[0], 168.669+puf_cali[1], 392.067+puf_cali[2], 158.369, 18.949, -8.714],
            [360.119+puf_cali[0], 369.628+puf_cali[1], 392.067+puf_cali[2], 158.369, 18.949, -8.714],
            [360.119+puf_cali[0], 369.628+puf_cali[1], 429.750, 158.369, 18.949, -8.714]
        ]
tea_and_egg = [195.504, 335.833, 429.29, 158.36, 18.949, -8.691]
egg =   [
            [147.546+egg_cali[0], 366.045+egg_cali[1], 421.444, 158.36, 18.949, -8.691],
            [147.546+egg_cali[0], 366.045+egg_cali[1], 392.934+egg_cali[2], 158.36, 18.949, -8.691],
            [147.700+egg_cali[0], 284.027+egg_cali[1], 392.297+egg_cali[2], 158.363, 18.947, -8.725],
            [147.546+egg_cali[0], 367.045+egg_cali[1], 392.934+egg_cali[2], 158.36, 18.949, -8.691],
            [147.546+egg_cali[0], 367.045+egg_cali[1], 421.444, 158.36, 18.949, -8.691],
        ]

axis_calibration =  [   
                        [0,0,0],
                        [0,0,0],
                        [0,0,0]
                    ]


# DEFAULT_VELOCITY = 100
# DEFAULT_ACCELERATION = 100

WORK_BASE = 30
WORK_TOOL = 10

VACUUM_PIN = 2

PHOTO_POSE = [0.00, 0.00, 0.00, 0.00, -90.00, 0.00]
# OBJECT_POSE = [20.00, 0.00, 0.00, 0.00, -90.00, 0.00]
OBJECT_POSE = [-67.517, 361.753, 293.500, 180.00, 0.00, 100.572]
PLACE_POSE = [-20.00, 0.00, 0.00, 0.00, -90.00, 0.00]
dis_place = [0.0, 368.0, 15.22, -180.0, 0.0, 90.0]
home =  [0.0, 368.0, 293.50, -180.0, 0.0, 90.0]

home_high =  [0.0, 368.0, 310.50, -180.0, 0.0, 90.0]
dis_point = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
joint_dis = [0.00, 0.00, 0.00, 0.00, -90.00, 0.00]
# 開袋點位

# only for example as we don't use yolo here
# assume NUM_OBJECTS=5, then this process will loop 5 times
NUM_OBJECTS = 0

tea_used = 0
puf_used = 0
egg_used = 0

class States(Enum):
    INIT = 0
    FINISH = 1
    MOVE_TO_PHOTO_POSE = 2
    YOLO_DETECT = 3
    MOVE_TO_OPJECT_TOP = 4
    PICK_OBJECT = 5
    MOVE_TO_PLACE_POSE = 6
    CHECK_POSE = 7
    CLOSE_ROBOT = 8
    GO_HOME = 9
    GO_TEA = 10
    GO_PUFF =11
    GO_EGG = 12

class ExampleStrategy(Node):
    
    def __init__(self):
        super().__init__('example_strategy')
        self.hiwin_client = self.create_client(RobotCommand, 'hiwinmodbus_service')
        self.object_pose = None
        self.object_cnt = 0

    def move_PTP(self,dis,hold = True,base = WORK_BASE,tool = WORK_TOOL):
        pose = Twist()
        [pose.linear.x, pose.linear.y, pose.linear.z] = dis[0:3]
        [pose.angular.x, pose.angular.y, pose.angular.z] = dis[3:6]
        req = self.generate_robot_request(
            cmd_mode=RobotCommand.Request.PTP,
            holding=hold,
            tool=tool,
            base=base,
            pose=pose,
        )
        res = self.call_hiwin(req)
        return res

    def slow_move_PTP(self,dis,hold = True,base = WORK_BASE,tool = WORK_TOOL):
        pose = Twist()
        [pose.linear.x, pose.linear.y, pose.linear.z] = dis[0:3]
        [pose.angular.x, pose.angular.y, pose.angular.z] = dis[3:6]
        req = self.generate_robot_request(
            cmd_mode=RobotCommand.Request.PTP,
            holding=hold,
            tool=tool,
            base=base,
            pose=pose,
            velocity = 50,
            acceleration = 50
        )
        res = self.call_hiwin(req)
        return res


    def move_LIN(self,dis,hold = True,base = WORK_BASE,tool = WORK_TOOL):
        pose = Twist()
        [pose.linear.x, pose.linear.y, pose.linear.z] = dis[0:3]
        [pose.angular.x, pose.angular.y, pose.angular.z] = dis[3:6]
        req = self.generate_robot_request(
            cmd_mode=RobotCommand.Request.LINE,
            digital_output_cmd=RobotCommand.Request.DIGITAL_OFF,
            velocity=255,
            acceleration=255,
            tool = tool,
            base = base,
            holding=hold,
            pose=pose
        )
        res = self.call_hiwin(req)
        
        return res
    

    def move_Angle(self,joint_dist,hold = True,base = WORK_BASE,tool = WORK_TOOL):
        pose = Twist()
        req = self.generate_robot_request(
            cmd_type=RobotCommand.Request.JOINTS_CMD,
            joints=joint_dist,
            holding=hold,
            tool = tool,
            base = base,
            pose=pose
            )
        res = self.call_hiwin(req)
        if res.arm_state == RobotCommand.Response.IDLE:
            return res
        else:
            res = self.call_hiwin(req)   
    
    def take_item(self,base = WORK_BASE,tool = WORK_TOOL):
        pose = Twist()
        req = self.generate_robot_request(
            cmd_mode=RobotCommand.Request.WAITING
        )
        res = self.call_hiwin(req)
        req = self.generate_robot_request(
            cmd_mode=RobotCommand.Request.DIGITAL_OUTPUT,
            digital_output_cmd=RobotCommand.Request.DIGITAL_ON,
            digital_output_pin=VACUUM_PIN,
            holding=True,
            tool = tool,
            base = base,
            pose=pose
        )
        res = self.call_hiwin(req)
        return res
        

    def put_item(self,base = WORK_BASE,tool = WORK_TOOL):
        pose = Twist()
        req = self.generate_robot_request(
            cmd_mode=RobotCommand.Request.WAITING
        )
        res = self.call_hiwin(req)
        req = self.generate_robot_request(
            cmd_mode=RobotCommand.Request.DIGITAL_OUTPUT,
            digital_output_cmd=RobotCommand.Request.DIGITAL_OFF,
            digital_output_pin=VACUUM_PIN,
            holding=True,
            tool = tool,
            base = base,
            pose=pose
        )
        res = self.call_hiwin(req)
        return res
       
    def Stop(self):
        con = input("Continue(Y/N)? :")
        if con == 'Y' or con == 'y':
            pass
        else:
            return

    def Now_pose(self):
        req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.CHECK_POSE)
        res = self.call_hiwin(req)
        print(res.current_position)
        return res
       
    def _state_machine(self, state: States) -> States:
        global tea_used,puf_used,egg_used,bag_mouth
        if state == States.INIT:
            self.get_logger().info('INIT')
            nest_state = States.GO_TEA

        elif state == States.GO_TEA:
            self.get_logger().info('GO_TEA')
            res = self.move_PTP(standby,False)
            res = self.move_PTP(tea[0])
            new_tea = tea[0].copy()
            while ac.next_go :
                if ac.start_ac:
                    print("Tea cali")
                    # print(new_tea)
                    print("Present tea =tea[0] "+str(new_tea))
                    new_tea[0] = tea[0][0]+ac.tea_x.get()
                    new_tea[1] = tea[0][1]+ac.tea_y.get()
                    new_tea[2] = tea[0][2]+ac.tea_z.get()
                    ac.start_ac = False
                    print("New tea = "+str(new_tea))
                    res = self.move_LIN(new_tea)
                else:
                    continue

            ac.next_go = True
            print(new_tea)
            new_tea2 = new_tea.copy()
            new_tea2[2] = tea[1][2]
            res = self.move_LIN(new_tea2)
            print(new_tea2)
            new_tea3 = new_tea2.copy()
            while ac.next_go :
                if ac.start_ac:
                    print("Tea cali")
                    print("Present tea = "+str(new_tea2))
                    new_tea3[0] = tea[1][0]+ac.tea_x.get()
                    new_tea3[1] = tea[1][1]+ac.tea_y.get()
                    new_tea3[2] = tea[1][2]+ac.tea_z.get()
                    ac.start_ac = False
                    print("New tea = "+str(new_tea3))
                    res = self.move_LIN(new_tea3)
                else:
                    continue
              
            ac.next_go = True  
            new_tea4 = new_tea3.copy()
            new_tea4[2] = new_tea[2]
            res = self.move_LIN(new_tea4)     
            if res.arm_state == RobotCommand.Response.IDLE:
                nest_state = States.GO_PUFF
            else:
                nest_state = None

        elif state == States.GO_PUFF:
            self.get_logger().info('GO_PUFF')
            # res = self.move_PTP(standby,False)
            res = self.move_PTP(tea_and_puf,False)
            res = self.move_PTP(puf[0])
            new_puf = puf[0]
            new_puf = puf[0].copy()
            while ac.next_go :
                if ac.start_ac:
                    print("Puff cali")
                    new_puf[0] = puf[0][0]+ac.puf_x.get()
                    new_puf[1] = puf[0][1]+ac.puf_y.get()
                    new_puf[2] = puf[0][2]+ac.puf_z.get()
                    ac.start_ac = False
                    res = self.move_LIN(new_puf)
                else:
                    continue

            
            new_puf2 = new_puf.copy()
            new_puf2[2] = puf[1][2]
            res = self.move_LIN(new_puf2)

            ac.next_go = True
            res = self.move_LIN(new_puf2)
            new_puf3 = new_puf2.copy()
            while ac.next_go :
                if ac.start_ac:
                    print("Puff cali")
                    new_puf3[0] = puf[1][0]+ac.puf_x.get()
                    new_puf3[1] = puf[1][1]+ac.puf_y.get()
                    new_puf3[2] = puf[1][2]+ac.puf_z.get()
                    ac.start_ac = False
                    res = self.move_LIN(new_puf3)
                else:
                    continue
            ac.next_go = True

            new_puf4 = new_puf3.copy()
            new_puf4[2] = new_puf[2]
            res = self.move_LIN(new_puf4)

            res = self.move_PTP(new_puf) 
            if res.arm_state == RobotCommand.Response.IDLE:
                nest_state = States.GO_EGG
            else:
                nest_state = None

        elif state == States.GO_EGG:
            self.get_logger().info('GO_EGG')
            # res = self.move_PTP(standby,False)
            res = self.move_PTP(tea_and_puf,False)
            res = self.move_PTP(tea_and_egg,False)
            res = self.move_PTP(egg[0])
            new_egg = egg[0].copy()
            while ac.next_go :
                if ac.start_ac:
                    print("EGG cali")
                    new_egg[0] = egg[0][0]+ac.egg_x.get()
                    new_egg[1] = egg[0][1]+ac.egg_y.get()
                    new_egg[2] = egg[0][2]+ac.egg_z.get()
                    ac.start_ac = False
                    res = self.move_LIN(new_egg)
                else:
                    continue
            ac.next_go = True
            new_egg2 = new_egg.copy()
            new_egg2[2] = egg[1][2]
            res = self.move_LIN(new_egg2)
            new_egg3 = new_egg2.copy()
            while ac.next_go :
                if ac.start_ac:
                    print("EGG cali")
                    new_egg3[0] = egg[1][0]+ac.egg_x.get()
                    new_egg3[1] = egg[1][1]+ac.egg_y.get()
                    new_egg3[2] = egg[1][2]+ac.egg_z.get()
                    ac.start_ac = False
                    res = self.move_LIN(new_egg3)
                else:
                    continue
            ac.next_go = True 
            new_egg4 = new_egg3.copy()
            new_egg4[2] = new_egg[2]
            res = self.move_LIN(new_egg4)
            if res.arm_state == RobotCommand.Response.IDLE:
                nest_state = States.GO_HOME
            else:
                nest_state = None    

        elif state == States.GO_HOME:
            self.get_logger().info('GO HOME')
            res = self.move_Angle(PHOTO_POSE)
            axis_calibration =  [   
                                    [ac.tea_x.get()+tea_cali[0],ac.tea_y.get()+tea_cali[1],ac.tea_z.get()+tea_cali[2]],
                                    [ac.puf_x.get()+puf_cali[0],ac.puf_y.get()+puf_cali[1],ac.puf_z.get()+puf_cali[2]],
                                    [ac.egg_x.get()+egg_cali[0],ac.egg_y.get()+egg_cali[1],ac.egg_z.get()+egg_cali[2]]
                                ]
            axis_txt = open('src/competition/axis_calibration.txt','w+')
            for i in range(0,3):
                for j in range(0,3):
                    axis_txt.write(str(axis_calibration[i][j])+' ')
                axis_txt.write('\n')
            axis_txt.close()
            ac.win.destroy()     
            
            if res.arm_state == RobotCommand.Response.IDLE:
                nest_state = States.CLOSE_ROBOT
            else:
                nest_state = None
        
        
        elif state == States.CHECK_POSE:
            self.get_logger().info('CHECK_POSE')
            req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.CHECK_JOINT)
            res = self.call_hiwin(req)
            print(res.current_position)
            if res.arm_state == RobotCommand.Response.IDLE:
                nest_state = States.FINISH
            else:
                nest_state = None

        elif state == States.CLOSE_ROBOT:
            self.get_logger().info('CLOSE_ROBOT')
            req = self.generate_robot_request(cmd_mode=RobotCommand.Request.CLOSE)
            res = self.call_hiwin(req)
            nest_state = States.FINISH

        else:
            nest_state = None
            self.get_logger().error('Input state not supported!')
            # return
        return nest_state

    def _main_loop(self):
        state = States.INIT
        while state != States.FINISH:
            state = self._state_machine(state)
            if state == None:
                break 
        self.destroy_node()  


    def _wait_for_future_done(self, future: Future, timeout=-1):
        time_start = time.time()
        while not future.done():
            time.sleep(0.01)
            if timeout > 0 and time.time() - time_start > timeout:
                self.get_logger().error('Wait for service timeout!')
                return False
        return True
    
    def generate_robot_request(
            self, 
            holding=True,
            cmd_mode=RobotCommand.Request.PTP,
            cmd_type=RobotCommand.Request.POSE_CMD,
            velocity=DEFAULT_VELOCITY,
            acceleration=DEFAULT_ACCELERATION,
            tool=1,
            base=WORK_BASE,
            digital_output_pin=0,
            digital_output_cmd=RobotCommand.Request.DIGITAL_OFF,
            pose=Twist(),
            joints=[float('inf')]*6,
            circ_s=[],
            circ_end=[],
            jog_joint=6,
            jog_dir=0
            ):
        request = RobotCommand.Request()
        request.digital_output_pin = digital_output_pin
        request.digital_output_cmd = digital_output_cmd
        request.acceleration = acceleration
        request.jog_joint = jog_joint
        request.velocity = velocity
        request.tool = tool
        request.base = base
        request.cmd_mode = cmd_mode
        request.cmd_type = cmd_type
        request.circ_end = circ_end
        request.jog_dir = jog_dir
        request.holding = holding
        request.joints = joints
        request.circ_s = circ_s
        request.pose = pose
        return request

    def call_hiwin(self, req):
        while not self.hiwin_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info('service not available, waiting again...')
        future = self.hiwin_client.call_async(req)
        if self._wait_for_future_done(future):
            res = future.result()
        else:
            res = None
        return res

    def call_yolo(self):
        class YoloResponse(NamedTuple):
            has_object: bool
            object_pose: list
        has_object = True if self.object_cnt < 5 else False
        object_pose = OBJECT_POSE
        res = YoloResponse(has_object,object_pose)
        # res.has_object = True if self.object_cnt < 5 else False
        # res.object_pose = OBJECT_POSE
        self.object_cnt += 1
        return res

    def start_main_loop_thread(self):
        self.main_loop_thread = Thread(target=self._main_loop)
        self.main_loop_thread.daemon = True
        self.main_loop_thread.start()
       
def axis_calib():
    rclpy.init()
    stratery = ExampleStrategy()
    stratery.start_main_loop_thread()
    rclpy.spin(stratery)
    rclpy.shutdown()

def main(args=None):

    # 建立一個子執行緒
    gui = threading.Thread(target = axis_calib)
    # 執行該子執行緒
    gui.start()
    ac.axis_cal()


if __name__ == "__main__":
    
    main()