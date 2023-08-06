import time


def fly_tello():
    from mrdrone import tello  # 引入tello包
    drone = tello.Tello()  # 初始化
    drone.streamon()  # 打开视频流并显示视频
    drone.takeoff()  # 起飞
    drone.forward(100)  # 前进100cm
    drone.cw(90)  # 旋转90°
    drone.flip('l')  # 左翻滚
    drone.land()  # 降落


def fly_folk():
    from mrdrone import folk  # 引入folk包，第一次使用时需要运行FolkTools.exe文件进行激活
    uav = folk.Folk()  # 初始化
    uav.stream_on()  # 打开视频流
    uav.stream_show()  # 显示视频流
    uav.takeoff()  # 起飞
    # uav.forward(100)  # 前进100cm
    # uav.turn_right(90)  # 旋转90°
    # uav.flip_left()  # 左翻滚
    uav.up(50)  # 上升50cm
    uav.land()  # 降落


if __name__ == '__main__':
    # fly_tello()
    fly_folk()
