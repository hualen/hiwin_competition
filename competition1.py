#!/usr/bin/env python3
import time
import rclpy
from enum import Enum
from threading import Thread
from rclpy.node import Node
from rclpy.task import Future
from typing import NamedTuple
from geometry_msgs.msg import Twist

from hiwin_interfaces.srv import RobotCommand
# from YoloDetector import YoloDetectorActionClient

from Ax12 import Ax12
import ax12move as mm
import order

'''
    read axis
'''
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

"""
    start motor setting
"""
# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = '/dev/ttyUSB0'
# Ax12.DEVICENAME = '/dev/ttyUSB1'

Ax12.BAUDRATE = 1_000_000
Ax12.DEBUG = True
# sets baudrate and opens com port
Ax12.connect()

# create AX12 instance with ID 10 
motor_id = 1
my_dxl = Ax12(motor_id)  
my_dxl.set_moving_speed(700)
my_dxl.print_status
"""
    end motor setting
"""

DEFAULT_VELOCITY = 100 
DEFAULT_ACCELERATION = 100
WORK_BASE = 4
ITEM_BASE = 6

VACUUM_PIN = 2
START_BUTTON = 2

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
open_bag =  [   
                # BASE 6
                [  76.328,  197.461,  219.289,  179.678,    0.603, -178.988], # 到袋子上方
                [  76.328,  197.461,  130.071,  179.678,    0.603, -178.988], # 吸袋子
                [  76.328,  136.196,  404.095,  179.678,    0.603, -178.988], # 提起袋子
                # BASE 4    
                [ 355.036,  296.641,  416.286,  179.764,    0.585, 90.4], # 移到卡扣上方
                [ 355.036,  296.641,  170.834,  179.775,    0.605, 90.503], # 降低至卡扣前
                [ 544.536,  296.641,  175.834,  179.775,    0.605, 90.503], # 進卡扣
                [ 544.536,  296.641,  424.883,  179.775,    0.605, 90.503], # 抬起打開紙袋
                [ 544.536,  296.641,  291.289,  179.775,    0.605, 90.503], # 放下一點
                [ 332.086,  296.641,  286.289,  179.775,    0.605, 90.503], # 抽出紙袋
                [196.584, 184.122, 422.637, 141.523, 0.448, 90.397], # 到旋轉袋子位置
                [196.584, 184.122, 276.912, 141.523, 0.448, 90.397], # 放下袋子
                [ 124.936,  184.124,  295.388,  179.775,    0.605, 90.503], # x減一點
                [ 124.936,  184.124,  126.208,  179.775,    0.605, 90.503], # z減一點
                [ 325.595,  184.124,  126.208,  179.775,    0.605, 90.503], # 往牆推
                [ 224.995,  184.124,  470.873,  179.775,    0.605, 90.503], # 歸位
                [ 374.995,  200.124,  470.873,  179.775,    0.605, 90.503]  # 歸位
            ]   
# 準備位置
standby =   [  70.817,  -29.797,  411.262,  179.678,    0.603, -178.988]
passby  =   [ 640.230,   90.990,  500.517,  179.775,    0.605,   90.503] 
# 五盒紅茶
tea =   [   
                # BASE 6
                [  39.134,  200.654,  272.428,  160.573,    0.731, -179.217], # 到紅茶上方
                [  39.134,  200.654,  180.666,  160.573,    0.731, -179.217], # 吸紅茶
                [  39.134,  155.840,  325.078,  160.573,    0.731, -179.217], # 提起袋子
        ]  

# 泡芙點位
puf =   [   
                # BASE 6
                [ 217.278,   88.715,  129.438,  158.236,    0.608,  178.428], # 到泡芙袋口
                [ 217.278,  153.438,  129.438,  158.236,    0.608,  178.428], # 往前推取泡芙
                [ 217.278,   72.528,  317.904,  158.236,    0.608,  178.428], # 抬起泡芙
                # BASE 4
                [ 490.482,   62.006,  448.429,  158.383,    0.650,   90.042], # pass
                [ 300.383+puf_cali[0],  208.606+puf_cali[1],  448.429+puf_cali[2],  158.383,    0.650,   90.042], # 到袋口
                [ 300.383+puf_cali[0],  208.606+puf_cali[1],  358.429+puf_cali[2],  158.383,    0.650,   90.042], # 進去袋口
        ]

# 奇趣蛋點位
egg =   [
                #BASE 6
                [355.411, 111.404, 255.954, 179.405, 0.635, 179.179],
                [355.411, 111.404, 198.755, 179.405, 0.635, 179.179],
                [345.411,  91.404, 314.938, 179.405, 0.635, 179.179],
                #BASE 4
                [ 408.668+egg_cali[0],  184.124+egg_cali[1],  500.211+egg_cali[2],  179.775,    0.605,    10.503], #
                [ 408.668+egg_cali[0],  184.124+egg_cali[1],  356.440+egg_cali[2],  179.775,    0.605,    10.503]
        ]
# 袋口
bag_mouth   =   [ 408.668+tea_cali[0],  184.124+tea_cali[1],  500.211+tea_cali[2],  179.775,    0.605, 90.503]
tea_enter   =   [
                    [ 398.668+tea_cali[0],  184.124+tea_cali[1],  280.224+tea_cali[2],  179.775,    0.605, 90.503], # 1st
                    [ 428.668+tea_cali[0],  184.124+tea_cali[1],  310.440+tea_cali[2],  179.775,    0.605, 90.503],
                    [ 398.668+tea_cali[0],  184.124+tea_cali[1],  356.440+tea_cali[2],  179.775,    0.605, 90.503] # 3rd
                ]   
enbgpf      =   [ -18.763,  344.999,  250.608, -180.000,    0.000, 90.0]
put_tea     =   [  45.989,  345.148,  116.915, -180.000,    0.000, 90.0]
# 出貨
out_bag =   [   
                [ 549.459,   45.836,  437.308,  179.775,    0.605, 90.503], # 到木板上方
                [ 549.459,   45.836,  220.865,  179.775,    0.605, 90.503], # PTP下去
                [ 549.459,   45.836,  147.412,  179.775,    0.605, 90.503], # 碰木板
                [ 549.459,   45.836,  200.865,  179.775,    0.605, 90.503], # 抬起一點
                [ 549.459,  179.124,  209.797,  179.775,    0.605, 90.503], # 至推戴位置
                [ 549.459,  179.124,  189.797,  179.775,    0.605, 90.503], # 至推戴位置
                [
                    [-148.746,  179.124,  189.797,  179.775,    0.605, 90.503],
                    [ -23.520,  179.124,  189.797,  179.775,    0.605, 90.503],
                    [  74.746,  179.124,  189.797,  179.775,    0.605, 90.503],
                    [ 187.227,  179.124,  189.797,  179.775,    0.605, 90.503]
                ], # 推袋子
                [ 549.459,   40.443,  220.865,  179.775,    0.605, 90.503], # 回木板位置
                [ 549.459,   40.443,  147.858,  179.775,    0.605, 90.503], # 放下木板
                [ 549.459,   40.443,  220.865,  179.775,    0.605, 90.503], # 回木板位置
            ]
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
    YOLO_DETECT = 9
    MOVE_TO_OPJECT_TOP = 4
    PICK_OBJECT = 5
    MOVE_TO_PLACE_POSE = 6
    CHECK_POSE = 7
    CLOSE_ROBOT = 8
    WATING_START = 3

class ExampleStrategy(Node):

    def __init__(self):
        super().__init__('example_strategy')
        self.hiwin_client = self.create_client(RobotCommand, 'hiwinmodbus_service')
        self.object_pose = None
        self.object_cnt = 0


    def move_PTP(self,dis,hold = True,base = WORK_BASE,tool = 1):
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
        if hold:
            if res.arm_state == RobotCommand.Response.IDLE:
                return res
            else:
                res = self.call_hiwin(req)
                return res
        else:
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


    def move_LIN(self,dis,hold = True,base = WORK_BASE,tool = 1):
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
        if hold:
            if res.arm_state == RobotCommand.Response.IDLE:
                return res
            else:
                res = self.call_hiwin(req)
                return res
        else:
            return res
    
    def slow_move_LIN(self,dis,hold = True,base = WORK_BASE,tool = 1):
        pose = Twist()
        [pose.linear.x, pose.linear.y, pose.linear.z] = dis[0:3]
        [pose.angular.x, pose.angular.y, pose.angular.z] = dis[3:6]
        req = self.generate_robot_request(
            cmd_mode=RobotCommand.Request.LINE,
            digital_output_cmd=RobotCommand.Request.DIGITAL_OFF,
            velocity=60,
            acceleration=60,
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
            cmd_mode=RobotCommand.Request.DIGITAL_OUTPUT,
            digital_output_cmd=RobotCommand.Request.DIGITAL_ON,
            digital_output_pin=VACUUM_PIN,
            holding=False,
            tool = tool,
            base = base,
            pose=pose
        )
        res = self.call_hiwin(req)
        return res
        

    def put_item(self,base = WORK_BASE,tool = 1):
        pose = Twist()

        req = self.generate_robot_request(
            cmd_mode=RobotCommand.Request.DIGITAL_OUTPUT,
            digital_output_cmd=RobotCommand.Request.DIGITAL_OFF,
            digital_output_pin=VACUUM_PIN,
            holding=False,
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


    def _state_machine(self, state: States) -> States:
        global tea_used,puf_used,egg_used
        if state == States.INIT:
            self.get_logger().info('INIT')
            nest_state = States.WATING_START

        elif state == States.WATING_START:
            self.get_logger().info('WATING_START')
            req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.READ_DI,
                digital_input_pin=START_BUTTON,
                holding=False
            )
            res = self.call_hiwin(req)
            if res.digital_state:
                nest_state = States.MOVE_TO_PHOTO_POSE
            else:
                nest_state = States.WATING_START

        elif state == States.MOVE_TO_PHOTO_POSE:     
            self.get_logger().info('START_WORK')
            for i in range(0,4):
                if forder[i][0] == 0 and forder[i][1] == 0 and forder[i][2] == 0:
                    continue
                else:
                    pass
                # 開袋子====================
                # res = self.move_PTP(standby,False,ITEM_BASE) 
                # mm.motor_move(my_dxl,525)
                # res = self.move_PTP(open_bag[0],False,ITEM_BASE) # 到袋子上方
                # res = self.move_LIN(open_bag[1],True,ITEM_BASE) # 吸袋子
                # res = self.take_item()
                # res = self.move_LIN(open_bag[2],True,ITEM_BASE) # 提起袋子
                # res = self.slow_move_PTP(open_bag[3],False) # 移到卡扣上方1
                # res = self.move_LIN(open_bag[4],False) # 降低至卡扣前
                # res = self.move_LIN(open_bag[5],False) # 進卡扣
                # res = self.move_LIN(open_bag[6],False) # 抬起打開紙袋
                # res = self.move_LIN(open_bag[7],False) # 放下一點
                # res = self.move_LIN(open_bag[8],False) # 抽出紙袋
                # res = self.move_PTP(open_bag[9]) # 到旋轉袋子位置
                # mm.motor_move(my_dxl,204)
                # time.sleep(1)
                # res = self.move_LIN(open_bag[10]) # 放下袋子
                # time.sleep(0.1)
                # res = self.put_item()
                # res = self.move_PTP(open_bag[11],False) # x減一點
                # res = self.move_PTP(open_bag[12],False) # z減一點
                # res = self.move_LIN(open_bag[13],False) # 往牆推
                # res = self.move_PTP(open_bag[14],False) # 歸位
                # res = self.move_PTP(open_bag[15]) # 歸位
                
                # 取物品=====================
                print("start order",i+1)
                # take tea
                for tea_num in range (0,forder[i][0]):
                    res = self.move_PTP(standby,False,ITEM_BASE)
                    mm.motor_move(my_dxl,525)
                    print("taketime.sleep(1) tea",tea_num+1)
                    # 拿取物品
                    res = self.move_PTP(tea[2],False,ITEM_BASE)
                    res = self.move_LIN(tea[1],True,ITEM_BASE)
                    res = self.take_item()
                    res = self.move_LIN(tea[2],False,ITEM_BASE)
                    res = self.slow_move_PTP(passby,False)
                    # 放置物品
                    res = self.slow_move_PTP(bag_mouth,False) # 移動到袋口
                    self.Stop
                    res = self.move_LIN(tea_enter[tea_num]) # 放下紅茶
                    res = self.put_item()
                    res = self.move_LIN(bag_mouth,False)# 回到袋口
                tea_used = tea_used + forder[i][0]

                # take puff========================================
                for puf_num in range (0,forder[i][1]):
                    res = self.move_PTP(standby,False,ITEM_BASE)
                    print("take puff",puf_num+1)
                    # 拿取物品
                    res = self.move_PTP(puf[0],False,ITEM_BASE)
                    mm.motor_move(my_dxl,254)
                    res = self.move_LIN(puf[1],True,ITEM_BASE)
                    res = self.take_item()
                    res = self.move_LIN(puf[2],False,ITEM_BASE)
                    # 放置物品
                    res = self.slow_move_PTP(puf[3],False) # 移動到袋口
                    res = self.slow_move_PTP(puf[4],False) # 移動到袋口
                    res = self.move_LIN(puf[5])
                    res = self.put_item()
                    res = self.move_LIN(puf[4],False)
                    
                puf_used = puf_used + forder[i][1]
                # if forder[i][1] != 0:
                #     mm.motor_move(my_dxl,525)
                # else:
                #     pass    

                # take egg
                for egg_num in range (0,forder[i][2]):
                    mm.motor_move(my_dxl,525)
                    res = self.move_PTP(standby,False,ITEM_BASE)
                    print("take egg",egg_num+1)
                    # 拿取物品
                    res = self.move_PTP(egg[0],False,ITEM_BASE)
                    res = self.move_LIN(egg[1],True,ITEM_BASE)
                    res = self.take_item()
                    res = self.move_LIN(egg[2],False,ITEM_BASE)
                    # 放置物品
                    res = self.slow_move_PTP(egg[3],False)# 移動到袋口
                    res = self.move_LIN(egg[4])# 放進袋子內
                    res = self.put_item()
                    res = self.move_LIN(bag_mouth,False)# 回到袋口
                egg_used =egg_used + forder[i][2]

                # 出貨=====================
                mm.motor_move(my_dxl,525)
                res = self.move_PTP(out_bag[0],False) # 到木板上方
                res = self.move_PTP(out_bag[1],False) # PTP下去
                res = self.move_LIN(out_bag[2]) # 碰木板
                res = self.take_item() 
                res = self.move_LIN(out_bag[3],False) # 抬起一點
                res = self.move_PTP(out_bag[4],False) # 至推戴位置1
                res = self.move_PTP(out_bag[5],False) # 至推戴位置2
                res = self.move_LIN(out_bag[6][i],False) # 推袋子
                res = self.move_PTP(out_bag[6][i],False) # 回木板位置
                res = self.move_PTP(out_bag[7],False) # 放下木板
                res = self.move_LIN(out_bag[8]) # 回木板位置
                res = self.put_item() 
                res = self.move_LIN(out_bag[9],False) # 回木板位置
            
            res = self.move_Angle(PHOTO_POSE)
            if res.arm_state == RobotCommand.Response.IDLE:
                nest_state = States.FINISH
            else:
                nest_state = None

        elif state == States.YOLO_DETECT:
            self.get_logger().info('YOLO_DETECT')
            res = self.call_yolo()
            # OBJECT_POSE here for example, should get obj pose according to yolo result
            if res.has_object:
                self.object_pose = res.object_pose
                nest_state = States.MOVE_TO_OPJECT_TOP
            else:
                nest_state = States.CHECK_POSE
                # nest_state = States.CLOSE_ROBOT

        elif state == States.MOVE_TO_OPJECT_TOP:
            self.get_logger().info('MOVE_TO_OPJECT_TOP')
            pose = Twist()
            [pose.linear.x, pose.linear.y, pose.linear.z] = self.object_pose[0:3]
            [pose.angular.x, pose.angular.y, pose.angular.z] = self.object_pose[3:6]
            # pose.linear.z += 10
            req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.PTP,
                pose=pose)
            res = self.call_hiwin(req)
            if res.arm_state == RobotCommand.Response.IDLE:
                nest_state = States.PICK_OBJECT
            else:
                nest_state = None

        elif state == States.PICK_OBJECT:
            self.get_logger().info('PICK_OBJECT')
            pose = Twist()
            [pose.linear.x, pose.linear.y, pose.linear.z] = self.object_pose[0:3]
            [pose.angular.x, pose.angular.y, pose.angular.z] = self.object_pose[3:6]
            req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.LINE,
                holding=False,
                velocity=5,
                pose=pose
            )
            res = self.call_hiwin(req)
            
            print(res)
            req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.DIGITAL_OUTPUT,
                digital_output_cmd=RobotCommand.Request.DIGITAL_ON,
                digital_output_pin=VACUUM_PIN,
                holding=False,
                pose=pose
            )
            res = self.call_hiwin(req)

            pose.linear.z -= 30
            req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.LINE,
                pose=pose
            )
            res = self.call_hiwin(req)
            
            if res.arm_state == RobotCommand.Response.IDLE:
                nest_state = States.MOVE_TO_PLACE_POSE
            else:
                nest_state = None

        elif state == States.MOVE_TO_PLACE_POSE:
            self.get_logger().info('MOVE_TO_PLACE_POSE')
            pose = Twist()
            req = self.generate_robot_request(
                cmd_type=RobotCommand.Request.JOINTS_CMD,
                joints=PLACE_POSE,
                pose=pose)
            res = self.call_hiwin(req)

            req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.DIGITAL_OUTPUT,
                digital_output_cmd=RobotCommand.Request.DIGITAL_OFF,
                digital_output_pin=VACUUM_PIN,
                holding=True,
                pose=pose
            )
            res = self.call_hiwin(req)
            req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.WAITING
            )
            res = self.call_hiwin(req)
            if res.arm_state == RobotCommand.Response.IDLE:
                nest_state = States.MOVE_TO_PHOTO_POSE
            else:
                nest_state = None

        elif state == States.CHECK_POSE:
            self.get_logger().info('CHECK_POSE')
            req = self.generate_robot_request(
                cmd_mode=RobotCommand.Request.CHECK_JOINT)
            res = self.call_hiwin(req)
            print(res.current_position)
            if res.arm_state == RobotCommand.Response.IDLE:
                nest_state = States.CLOSE_ROBOT
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
            base=0,
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