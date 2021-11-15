# Raspberry-Pi-3631AS-Drive-3631AS-
Raspberry Pi 3631AS Drive 树莓派连接3631AS数码管驱动 控制显示代码


# 3631AS-1 共阴 数码管 驱动
# 使用前：根据py文件中的NUM_list列表和引脚图的1-12号（没有6） 在GPIO_list中填写你连接的对应的GPIO
# 使用方法：将本文件使用import drive_3631as导入 在不改变此文件名的前提下 
# 使用drive_3631as.start_3631AS(数字)开始显示 使用drive_3631as.stop_3631AS()结束显示 仅支持三位以内的int型或浮点型数据
