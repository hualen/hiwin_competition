#!/usr/bin/env python3
import time
import rclpy
from enum import Enum
from threading import Thread
from rclpy.node import Node
from rclpy.task import Future
from typing import NamedTuple
from geometry_msgs.msg import Twist
import order

from hiwin_interfaces.srv import RobotCommand
# from YoloDetector import YoloDetectorActionClient

from Ax12 import Ax12
import ax12move as mm

DEBUG_MODE = False


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

"""
    start order
"""
order.start_order()
forder = order.final_order 
print(forder)


DEFAULT_VELOCITY = 100
DEFAULT_ACCELERATION = 100
# DEFAULT_VELOCITY = 50
# DEFAULT_ACCELERATION = 50
WORK_BASE = 30

BAG_TOOL = 10
DRAWER_TOOL = 15

VACUUM_PIN = 2
START_BUTTON = 2

PHOTO_POSE = [0.00, 0.00, 0.00, 0.00, -90.00, 0.00]
# OBJECT_POSE = [20.00, 0.00, 0.00, 0.00, -90.00, 0.00]
OBJECT_POSE = [-67.517, 361.753, 293.500, 180.00, 0.00, 100.572]
PLACE_POSE = [-20.00, 0.00, 0.00, 0.00, -90.00, 0.00]
dis_point = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]



# 開袋點位
open_bag =  [   
                # BASE 30 TOOL 10
                [356.067, 198.464, 111.683, 158.365, 18.949, -8.696], # 轉治具並下降
                [511.463, 198.464, 111.683, 158.365, 18.949, -8.696], # 壓袋子
                [511.463, 268.12, 111.683, 158.365, 18.949, -8.696],  # 壓袋子位置前推
                [511.463, 268.12, 211.95, 158.365, 18.949, -8.696],   # 往上一點
                [506.462, 216.605, 244.391, 158.365, 18.949, -8.696], # 碰到繩子洞口  
                [302.169, 250.605, 254.391, 158.365, 18.949, -8.696], # 抬高中繼點
                [94.269, 285.991, 420.882, 158.366, 18.95, -8.696],  # 到原子筆口前 [94.269, 285.991, 410.882, 158.366, 18.95, -8.696]
                [0.792, 285.991, 420.883, 158.365, 18.949, -8.696],  # 進原子筆
                [0.792, 285.991, 380.309, 158.365, 18.949, -8.696],  # 下降一點
                [0.792, 257.941, 380.309, 158.365, 18.949, 1.696],   # y減躲避開鉤子
                [0.792, 257.941, 252.876, 158.365, 18.949, 1.696],   # 下降離開袋子
            ]   

# 收袋點位
out_bag =   [
                # [416.255, 200.401, 428.322, 158.363, 18.948, -8.696], # 至勾袋位置高點
                # [416.255, 200.401, 280.634, 158.363, 18.948, -8.696], # 至勾袋位置低點
                # [416.616, 280.918, 280.348, 158.362, 18.947, -8.696], # 前推至勾袋位置
                # [416.616, 280.918, 382.847, 158.362, 18.947, -8.696], # 上台使鉤子碰到
                # # [145.031, 221.175, 395.194, 158.363, 18.948, -8.696], # 袋口中繼點
                # [138.279, 270.897, 453.266, -169.409, 20.632, 2.475], # 到原子筆口前
                # [-69.019, 270.897, 453.266, -169.409, 20.632, 2.475], # 進入原子筆
                # [-79.019, 270.897, 401.141, -169.409, 20.632, 2.475], # 下降一點
                # [-79.019, 240.379, 401.141, -169.409, 20.632, 78.758],# y減躲避開鉤子
                # [47.042, 275.482, 254.341, 153.697, 9.848, 68.690], # 旋轉下降離開袋子-169.409, 20.632, 78.758
                [428.203, 215.629, 351.779, 158.361, 18.943, -8.706], # 至勾袋位置高點
                [428.203, 215.629, 279.904, 158.361, 18.943, -8.706], # 至勾袋位置低點
                [428.203, 282.391, 279.904, 158.361, 18.943, -8.706], # 前推至勾袋位置
                [428.203, 282.391, 322.621, 158.361, 18.943, -8.706], # 上台使鉤子碰到
                [446.905, 291.338, 395.194, 158.363, 18.948, -8.696], # 靠近螺絲口使繩子脫離
                
                [170.016, 231.337, 454.456, 158.362, 18.948, 91.509],
                [117.272, 287.338, 454.439, 158.362, 18.95, 91.51],
                [-76.189, 287.141, 454.435, 158.362, 18.952, 91.516],
                [-76.189, 287.141, 391.56, 158.362, 18.952, 91.516],
                [-76.189, 223.204, 391.56, 158.362, 18.952, 91.516],
                [-76.189, 223.204, 350.56, 158.362, 18.952, 91.516],
                [-76.189, 233.566, 350.035, 158.362, 18.952, 91.516],
                [-78.039, 237.591, 288.122, 157.566, -11.885, 91.465],
                [  0.464, 237.591, 288.122, 157.566, -11.885, 91.465]
            ]
standby_pass = [40.792, 153.685, 252.876, 158.365, 18.949, 1.696]
standby = [232.82, 260.402, 428.323, 158.364, 18.948, -8.696]

tea =   [
            [241.607+tea_cali[0], 365.833+tea_cali[1], 422.635, 158.364, 18.948, -8.696],
            [241.607+tea_cali[0], 365.833+tea_cali[1], 394.623, 158.364, 18.948, -8.696],
            [241.607+tea_cali[0], 196.554+tea_cali[1], 392.623, 158.364, 18.948, -8.696],
            [241.607+tea_cali[0], 379.157+tea_cali[1], 394.623, 158.364, 18.948, -8.696],
            [241.607+tea_cali[0], 364.833+tea_cali[1], 394.623, 158.364, 18.948, -8.696],
            [241.607+tea_cali[0], 364.833+tea_cali[1], 422.635, 158.364, 18.948, -8.696]
        ]
puf =   [#關到底
            [362.118+puf_cali[0], 366.628+puf_cali[1], 429.750, 158.368, 18.949, -8.713],
            [362.118+puf_cali[0], 366.628+puf_cali[1], 392.067, 158.368, 18.949, -8.713],
            [362.119+puf_cali[0], 187.153+puf_cali[1], 392.067, 158.369, 18.949, -8.714],
            [362.119+puf_cali[0], 368.628+puf_cali[1], 392.067, 158.369, 18.949, -8.714],
            [362.119+puf_cali[0], 368.628+puf_cali[1], 429.750, 158.369, 18.949, -8.714]
        ]
egg =   [
            [150.546+egg_cali[0], 366.045+egg_cali[1], 421.444, 158.36, 18.949, -8.691],
            [150.546+egg_cali[0], 366.045+egg_cali[1], 392.934, 158.36, 18.949, -8.691],
            [150.700+egg_cali[0], 290.027+egg_cali[1], 392.297, 158.363, 18.947, -8.725],
            [150.546+egg_cali[0], 367.045+egg_cali[1], 392.934, 158.36, 18.949, -8.691],
            [150.546+egg_cali[0], 367.045+egg_cali[1], 421.444, 158.36, 18.949, -8.691],
        ]
finish  =   [
                [45.504, 197.057, 390.29, -173.967, 25.277, 46.986],
                [-151.832, 127.657, 436.803, -173.967, 25.277, 46.986],
                [-219.982, 127.657, 436.803, -173.967, 25.277, 46.986],
                [-219.982, 131.532, 350.178, -173.967, 25.277, 46.986],
                [-15.62, 135.419, 350.178, -173.967, 25.277, 46.986], #x方向推
                [-15.62, 224.577, 350.178, -173.967, 25.277, 46.986], #y方向推
                # [-15.62, 204.74, 350.178, -173.967, 25.277, 46.986],
            ]

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
    WATING_START = 10

class ExampleStrategy(Node):
    
    def __init__(self):
        super().__init__('example_strategy')
        self.hiwin_client = self.create_client(RobotCommand, 'hiwinmodbus_service')
        self.object_pose = None
        self.object_cnt = 0

    def move_PTP(self,dis,hold = True,tool = BAG_TOOL,base = WORK_BASE):
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

    def slow_move_PTP(self,dis,hold = True,base = WORK_BASE,tool = 1):
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


    def move_LIN(self,dis,hold = True,tool = BAG_TOOL,base = WORK_BASE):
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
    

    def move_Angle(self,joint_dist,hold = True,base = WORK_BASE,tool = 1):
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
    
    def take_item(self,base = WORK_BASE,tool = 1):
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
        

    def put_item(self,base = WORK_BASE,tool = 1):
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
    
    def BStop(self):
        if not DEBUG_MODE:
            return
        self.get_logger().info('WAIT_START')
        while True:
            req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.READ_DI,
                digital_input_pin=6,
                holding=False
            )
            res = self.call_hiwin(req)
            if res.digital_state:
                break
            else:
                pass

       
    def _state_machine(self, state: States) -> States:
        global tea_used,puf_used,egg_used
        if state == States.INIT:
            self.get_logger().info('INIT')
            nest_state = States.WATING_START

        elif state == States.WATING_START:
            self.get_logger().info('WATING_START')
            req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.READ_DI, 
                digital_input_pin=2,
                holding=False
            )
            res = self.call_hiwin(req)
            if res.digital_state:
                nest_state = States.MOVE_TO_PLACE_POSE
            else:
                nest_state = States.WATING_START

        #===================================================
        # MOVE PTP
        #===================================================
        elif state == States.MOVE_TO_PLACE_POSE:
            self.get_logger().info('START_ORDER')
            for i in range(0,4):
                if forder[i][0] == 0 and forder[i][1] == 0 and forder[i][2] == 0:
                    continue
                else:
                    pass
                # 開袋子==================== 
                res = self.move_PTP(open_bag[0],False) # 到袋子上方
                
                res = self.move_PTP(open_bag[1],False) # 吸袋子
                
                res = self.move_PTP(open_bag[2],False) # 提起袋子
                
                res = self.move_PTP(open_bag[3],False) # 移到卡扣上方
            
                res = self.move_PTP(open_bag[4],False) # 降低至卡扣前
                
                res = self.move_PTP(open_bag[5],False) # 進卡扣
                
                res = self.move_PTP(open_bag[6],False) # 抬起打開紙袋
                
                res = self.move_PTP(open_bag[7],False) # 放下一點
                
                res = self.move_PTP(open_bag[8],False)
                
                res = self.move_PTP(open_bag[9],False)
                
                res = self.move_PTP(open_bag[10],False)
                
            
                # 取物品=====================
                print("start order",i+1)
                # take tea
                res = self.move_PTP(standby_pass,False)
                
                res = self.move_PTP(standby,False)
                
                if forder[i][0] != 0:
                    res = self.move_PTP(tea[0])
                    res = self.move_LIN(tea[1],False)
                    for tea_num in range (0,forder[i][0]):
                        print("take tea",tea_num+1)
                        res = self.move_LIN(tea[2],False)
                        res = self.move_LIN(tea[3],False)
                        
                    res = self.move_LIN(tea[4],False)
                    res = self.move_LIN(tea[5],False)
                    tea_used = tea_used + forder[i][0]    
                res = self.move_PTP(standby,False)
                if forder[i][1] != 0:
                    res = self.move_PTP(puf[0])
                    res = self.move_LIN(puf[1],False)
                    for puf_num in range (0,forder[i][1]):
                        print("take puf",puf_num+1)
                        res = self.move_LIN(puf[2],False)
                        res = self.move_LIN(puf[3],False)
                    res = self.move_LIN(puf[4],False)
                    
                    puf_used = puf_used + forder[i][0]
                res = self.move_PTP(standby,False)
                if forder[i][2] != 0:
                    res = self.move_PTP(egg[0])
                    res = self.move_LIN(egg[1],False)
                    for egg_num in range (0,forder[i][2]):
                        print("take egg",egg_num+1)
                        res = self.move_LIN(egg[1],False)
                        res = self.move_LIN(egg[2],False)
                        res = self.move_LIN(egg[3],False) 
                    res = self.move_LIN(egg[4],False)
                    egg_used = egg_used + forder[i][0]
                res = self.move_PTP(standby,False)

                # 收袋=====================
                res = self.move_PTP(out_bag[0],False) # 
                res = self.move_PTP(out_bag[1],False) #
                res = self.move_LIN(out_bag[2],False) #
                res = self.move_LIN(out_bag[3],False) # 
                res = self.move_PTP(out_bag[4],False) #
                res = self.move_PTP(out_bag[5],False) #
                res = self.move_PTP(out_bag[6]) # 
                res = self.move_LIN(out_bag[7],False) # 
                res = self.move_PTP(out_bag[8],False) 
                res = self.move_PTP(out_bag[9],False)
                
                res = self.move_PTP(out_bag[10],True)
                
                res = self.move_PTP(out_bag[11],True)
                
                res = self.move_PTP(out_bag[12],True)
                
                res = self.move_PTP(out_bag[13],True)
                
                 
                # 愛的魔力轉圈圈=====================
                res = self.move_PTP(finish[0],False) # 
                res = self.move_PTP(finish[1],False) #
                res = self.move_PTP(finish[2],False) # 
                res = self.move_PTP(finish[3],False) # 
                res = self.move_PTP(finish[4],False) # 
                res = self.move_PTP(finish[5],False) #
                # res = self.move_PTP(finish[6],True) #
            
            res = self.move_Angle(PHOTO_POSE)
            if res.arm_state == RobotCommand.Response.IDLE:
                nest_state = States.FINISH
            else:
                nest_state = None
        #===================================================
        # MOVE PTP END
        #===================================================
        
        
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
            tool=BAG_TOOL,
            base=WORK_BASE,
            digital_input_pin=START_BUTTON,
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
        request.digital_input_pin = digital_input_pin
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
       

def main(args=None):
    
    rclpy.init(args=args)
    stratery = ExampleStrategy()
    stratery.start_main_loop_thread()
    rclpy.spin(stratery)
    rclpy.shutdown()

if __name__ == "__main__":
    
    main()