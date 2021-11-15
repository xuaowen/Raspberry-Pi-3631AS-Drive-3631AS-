import drive_3631as
import time


for i in range(1,200):
    drive_3631as.start_3631AS(i)
    time.sleep(0.5)
    drive_3631as.stop_3631AS()