# 3631AS-1 共阴 数码管 驱动
# 徐奥雯编写   XUAOWEN-ASSETS  E-MAIL:CHINA@XUAOWEN.CN  WECHAT:US-00000
# 使用前：根据NUM_list和引脚图的1-12号（没有6） 在GPIO_list中填写你连接的对应的GPIO
# 使用方法：将本文件使用import drive_3631as导入 在不改变此文件名的前提下 
# 使用drive_3631as.start_3631AS(数字)开始显示 使用drive_3631as.stop_3631AS()结束显示 仅支持三位以内的int型或浮点型数据


import RPi.GPIO as GPIO
import time
from multiprocessing import Process

# 根据NUM_list和引脚图的1-12号（没有6） 在GPIO_list中填写你连接的对应的GPIO
NUM_list = [1, 2, 3, 4, 5, None, 7, 8 ,9, 10, 11, 12]  # 注意没有第6个  8,9,12 为共阴
GPIO_list = [5, 6, 13, 19, 26, None, 18, 16, 20, 23, 24, 21]  #填写你的GPIO  跳过None

#     __11_       |
#    |     |      |  
# 10 |     | 7    |  共三个数字  每个数字8个灯 （包括一个点） 
#    |__5__|      |  三个数字的GND阴级分别为8, 9, 12
#    |     |      |  某个灯要亮 必须其阳极为高电平且阴级为低电平 如果阳极与印记都为高点电平则不亮
#  1 |     | 4    |  
#    |__2__|      |  
#             *3  |

# 数码管的显示分为静态和动态两种。静态就是一个GPIO控制一个LED小灯管。
# 但是随着控制数码管数量的增加，GPIO口就占用太多了，所以多个数码管可以有 共阴 和 共阳 两种共享引脚。
# 这个时候如果采用静态点亮数码管的方式，共享引脚的数码管显示完全一样。
# 所谓动态方式，就是通过GPIO选择引脚，选择要点亮的某个数码管，然后通过共享引脚点亮LED小灯管。
# 然后快速切换点亮其他数码管，由于点亮的切换频率非常快所以感觉上数码管一直亮着。

GPIO.setmode(GPIO.BCM)  # 设置使用BCM引脚编号模式

for gpio_num in GPIO_list:
    if gpio_num :  # gpio_num不为None
        GPIO.setup(gpio_num, GPIO.OUT)  # 设置出


def num_print_only_one(number, address, point):
    '''传入参数（0-9）,位置（1-3）,是否有小数点（0/1）'''

    # 亮灯位置 此时未设置3,6,8,9,10,12  默认为0
    # 顺序是1-12   第6位不参与运行 设置为6
    number_light_list = [None, '110106100110', '000106100000', '110016100010', '010116100010', '000116100100', '010116000110',
                                '110116000110', '000106100010', '110116100110', '010116100110']
    
    number_light_coding = number_light_list[number+1]  # 获取对应亮灯编码 不含3,6,8,9,10,12
    number_light_coding_list = list(number_light_coding)  # 转成列表
    
    if address == 3:  # 确定第几个数字亮  共三个
        number_light_coding_list[8-1] = '0'
        number_light_coding_list[9-1] = '1'
        number_light_coding_list[12-1] = '1'
    elif address == 2:
        number_light_coding_list[8-1] = '1'
        number_light_coding_list[9-1] = '0'
        number_light_coding_list[12-1] = '1'
    elif address == 1:
        number_light_coding_list[8-1] = '1'
        number_light_coding_list[9-1] = '1'
        number_light_coding_list[12-1] = '0'

    number_light_coding_list[3-1] = str(point)  #确定小数点是否亮

    for i in range(0, 12):  # 循环执行  输出制定亮起的数字
        if number_light_coding_list[i] == '1':
            GPIO.output(GPIO_list[i], GPIO.HIGH)
        elif number_light_coding_list[i] == '0':
            GPIO.output(GPIO_list[i], GPIO.LOW)


def number_legal_test(number_01):
    '''输入合法检测'''
    if type(number_01) == type(1):  # 检测是否为int型
        if len(str(number_01)) > 3:  #检测是否位数过多
            print('数据过长，单个3631AS-1 最多显示三位数字')
        else:
            return 'int'  # 输入合法 int
    elif type(number_01) == type(1.0):  # 检测是否为float型
        if len(str(number_01)) > 4:  #检测是否位数过多  带小数点共四位
            print('数据过长，单个3631AS-1 最多显示三位数字')
        else:
            return 'float'  # 输入合法 float
    else:
        print('数据类型错误，请收入int型或float型数据')


def int_to_three(number_02):
    '''将两个或单个整数数字转换为三个'''
    str_number_02 = str(number_02)
    if len(str_number_02) == 1:
        return '00' + str_number_02
    elif len(str_number_02) == 2:
        return '0' + str_number_02
    else:
        return str(number_02)


def float_to_three(number_03):
    '''将两个浮点数字转换为三个'''
    str_number_03 = str(number_03)
    if len(str_number_03) == 3:
        return '0' + str_number_03
    else:
        return str(number_03)


def number_3631AS_start(number_three):
    '''显示三个数字'''
    if number_legal_test(number_three) == 'int':
        str_number_three = int_to_three(number_three)
        while 1:
            for i in range(1, 3+1):
                num_print_only_one(int(str_number_three[i-1]),i,0)  # 执行一个数字的显示
                time.sleep(1/250)

    elif number_legal_test(number_three) == 'float':
        str_number_three = float_to_three(number_three)
        point_index = str_number_three.find('.')  # 找到小数点
        str_number_three = str_number_three[:point_index] + str_number_three[point_index+1:]  # 去除小数点拼接
        if point_index == 2-1:  # 根据小数点位置
            point_list=[1,0,0]
        elif point_index == 3-1:
            point_list=[0,1,0]
        while 1:
            for i in range(1, 3+1):
                num_print_only_one(int(str_number_three[i-1]),i,point_list[i-1])  # 执行一个数字的显示
                time.sleep(1/250)


# 多进程 Liunx中多进程不必写在if __name__ == '__main__':内
def start_3631AS(number):
    global p01  # 全局变量
    # target=要开启的子进程的函数  name=进程的名字  args=传递参数（必须是元组类型）
    p01 = Process(target=number_3631AS_start, name='进程01', args=(number,))  # 实例化一个进程对象  
    p01.start()  # 开启一个子进程
def stop_3631AS():
    p01.terminate()  # 手动杀死子进程

    for gpio_num in GPIO_list:
        if gpio_num :  # gpio_num不为None
            GPIO.output(gpio_num, False)  # 关闭所有针脚


if __name__ == '__main__':
    start_3631AS(888)  # 开始显示 函数
    time.sleep(5)
    stop_3631AS()  # 结束显示 函数

# xuaowen XUAOWEN 徐奥雯






