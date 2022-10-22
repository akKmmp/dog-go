import socket
from imp import C_EXTENSION
from telnetlib import WILL
from typing_extensions import Self
import walk
import time

#-----------------------配置区域-------------------------#
walk_1 = walk.Unitree_Robot()  #调用SDK库
Middle = [0,0]                                             #中值变量
re = [0,0]
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #UPD接收
udp.bind(('', 4000))                           # 为服务器绑定一个固定的地址，ip和端口
a = 125
go = 1                                                      #直行速度
#------------------------------------------------------------#

#UPD接收
def cv_m():
    data,addr = udp.recvfrom(1024)
    #print(data.decode('utf-8') ) #打印接收的内容
    data = int(data)
    return data         #返回值

def no_1():         #倾倒
    motion_time = 0
    while motion_time <= 50:
        time.sleep(0.1)
        motion_time += 1
        if (motion_time >= 1 and motion_time < 5):              #停止
            state = walk_1.stop_walk()
        elif(motion_time >= 5 and motion_time < 30):            #直行
            state = walk_1.forward_walk(0.7,-0.05)
        if (motion_time >= 30 and motion_time < 35):            #停止，防止卡脚
            state = walk_1.stop_walk()
        elif (motion_time >= 35 and motion_time < 50):          #倾倒
            state = walk_1.robot_pose(1.9,0.0,0.0,0.0)
        print(motion_time)
        cv_m()

def no_2():                         #爬楼梯
    motion_time = 0
    while motion_time < 35:
        time.sleep(0.1)
        motion_time += 1
        if(motion_time >= 1 and motion_time < 13):
            state=walk_1.rightRotate_walk(1,-0.7,-0.1)
        if(motion_time >= 13):
            state=walk_1.robot_climb()
        print(motion_time)
        cv_m()

def no_3():
    motion_time = 0
    while motion_time < 45:
        time.sleep(0.1)
        motion_time += 1
        if motion_time >= 0 and motion_time <= 15:
            state = walk_1.forward_walk(go,0.1)
        elif motion_time > 15 and motion_time <= 25:
            state = walk_1.leftyaw_walk(0)
        elif motion_time > 25 and motion_time <= 35:
            state = walk_1.forward_walk(go,0.1)
        elif motion_time > 35:
            state = walk_1.rightyaw_walk(0)
        print(motion_time)
        cv_m()

#主函数c
def main():
    while True:
        Middle = 999
        Middle = cv_m()
        print("视觉返回值",Middle)
        #print(Middle[1])
        if(Middle == 11):       #倾倒检测
           no_1()
        elif(Middle == 12):#爬楼梯
            no_2()
        elif(Middle == 13): #避障
            no_3()
        elif(Middle == 0): 
            state = walk_1.forward_walk(go,0.1)      #直行
        #向左修正，(直行速度，旋转，侧向)
        elif(Middle == -1):
            state = walk_1.leftRotate_walk(go , 0.4 ,0.1)
        elif(Middle == -2):
            state = walk_1.leftRotate_walk(go , 0.6 ,0.1)
        #向右修正，(直行速度，旋转，侧向)
        elif(Middle == 1):
            state = walk_1.rightRotate_walk(go, -0.4 ,-0.1)
        elif(Middle == 2):
            state = walk_1. rightRotate_walk(go, -0.6 ,-0.1)
        
        # elif(Middle == -3):
        #     state = walk_1. forward_walk((0.4),-0.05)
        elif(Middle == 3):
            state = walk_1. Robot_rightRotate()         #转向
        else: 
            state = walk_1.stop_walk()          #停止
main()
