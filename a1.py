import socket
import walk
import time

#-----------------------配置区域-------------------------#
walk_1 = walk.Unitree_Robot()  #调用SDK库
Middle = [0,0]                                             #中值变量
re = [0,0]
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #UPD接收
udp.bind(('', 4000))                           # 为服务器绑定一个固定的地址，ip和端口
a = 125
go = 1.5                                                      #直行速度
#------------------------------------------------------------#

#UPD接收
def cv_m():
    data,addr = udp.recvfrom(1024)
    #print(data.decode('utf-8') ) #打印接收的内容
    data = int(data)
    return data         #返回值

def no_1():         #倾倒
    motion_time = 0
    while motion_time <= 30:
        time.sleep(0.1)
        motion_time += 1
        if (motion_time >= 1 and motion_time < 2):              #停止
            state = walk_1.stop_walk()
        elif(motion_time >= 2 and motion_time < 11):            #直行
            state = walk_1.forward_walk(go,-0.02)
        elif (motion_time >= 11 and motion_time < 14):            #停止，防止卡脚
            state = walk_1.stop_walk()
        elif (motion_time >= 14 and motion_time < 20):          #倾倒
            state = walk_1.robot_pose(2,0.0,0.0,0.0)
        elif(motion_time >= 20 ): 
            state = walk_1.forward_walk(go,-0.07)      #直行
        print(motion_time)
        cv_m()

def no_2():                         #爬楼梯
    motion_time = 0
    while motion_time < 27:
        time.sleep(0.1)
        motion_time += 1
        if(motion_time >= 1 and motion_time < 12):
            state=walk_1.rightRotate_walk(1,-0.6,0.05)
        elif(motion_time >= 12 and motion_time < 22):
            state=walk_1.robot_climb()
        elif(motion_time >= 22):
            state = walk_1.stop_walk()
        print(motion_time)
        cv_m()

def no_3():                         #避障
    motion_time = 0
    i = 0
    while i != 2:
        time.sleep(0.1)
        Middle = cv_m()
        motion_time += 1
        if motion_time >= 0 and motion_time <= 4:       #直行
            state = walk_1.forward_walk(go,-0.1)
        elif  motion_time > 4 and motion_time < 6:        #停止
            state = walk_1.stop_walk()
        elif motion_time > 6 and motion_time <= 12:        #向左平移
            state = walk_1.leftyaw_walk(0)
        elif  motion_time > 12 and motion_time<=13:       #停一下
            state = walk_1.stop_walk()
        elif motion_time > 13 and motion_time <= 20:        #直行
            state = walk_1.forward_walk(go,-0.1)
        elif motion_time > 20 and motion_time <=22:         #停一下
            state = walk_1.stop_walk() 
            i = 1

        elif i == 1 and Middle <= 1:
            a = 0
            while a < 2:
                time.sleep(0.1)
                a += 1
                state = walk_1.stop_walk() 
            i = 2
        elif (not Middle or Middle > 1) and i == 1:
            state = walk_1.rightyaw_walk(0)
        print(Middle)
        cv_m()

def no_4():                 #充电区域
    motion_time = 0
    while True:
        time.sleep(0.1)
        motion_time += 1
        Middle = cv_m()
        if motion_time <= 11:
            state = walk_1.forward_walk(go,-0.05)      #直行
        if motion_time > 11 :            #停止，防止卡脚
            state = walk_1.stop_walk()
        print(motion_time)

#主函数c
def main():
    i = 0
    while True:
        Middle = 999
        Middle = cv_m()
        print("视觉返回值",Middle)
        if(Middle == 11 and i == 1):       #倾倒检测
           no_4()   
        elif(Middle == 12):#爬楼梯
            no_2()
        elif(Middle == 11 and i == 0):       #倾倒检测
           no_1()
           i = 1
        elif(Middle == 13): #避障
            no_3()

        elif(Middle == 0): 
            state = walk_1.forward_walk(go,0.18)      #直行
        #向左修正，(直行速度，旋转，侧向)
        elif(Middle == -1):
            state = walk_1.leftRotate_walk(go , 0.4 ,0.1)
        elif(Middle == -2):
            state = walk_1.leftRotate_walk(go , 0.8 ,0.2)
        #向右修正，(直行速度，旋转，侧向)
        elif(Middle == 1):
            state = walk_1.rightRotate_walk(go, -0.4 ,-0.1)
        elif(Middle == 2):
            state = walk_1. rightRotate_walk(go, -0.8 ,-0.2)
        
        elif(Middle == 3):
            state = walk_1. Robot_rightRotate()         #转向
        else: 
            state = walk_1.stop_walk()          #停止
main()
