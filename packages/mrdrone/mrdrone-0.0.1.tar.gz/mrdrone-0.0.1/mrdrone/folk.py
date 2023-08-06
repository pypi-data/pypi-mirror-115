import os
import sys
import time
import threading
import warnings

from pyfolk import *
from pynput.keyboard import Key, Listener

warnings.filterwarnings("ignore", category=DeprecationWarning)  # 忽略弃用警告


class Folk:

    def __init__(self, equip_type='camera', fly_mode='dance'):

        self.led_flag = self.camera_flag = 0
        self.dance_flag = self.remote_flag = 0

        # 确定连接设备类型
        if equip_type == 'camera':
            self.equip_type = EquipmentType.CameraPlane  # 带有摄像头的无人机
            self.camera_flag = 1
        elif equip_type == 'led':
            self.equip_type = EquipmentType.LedPlane  # 带有灯带的无人机
            self.led_flag = 1
        else:
            self.equip_type = EquipmentType.Plane  # 没有配件的无人机

        self.uapi = UserApi()  # 实例化UserApi

        # 创建设备并连接设备
        _ret = self.uapi.plane_connect(self.equip_type, self.uapi.equipment_create(self.equip_type))
        if _ret:
            print('connect to equipment:', self.equip_type)
        else:
            print('connect error!')
            # os._exit(0)
            sys.exit()

        # 确定飞行模式
        if fly_mode == 'dance':
            self.uapi.dance_fly_entry_dance_mode(self.equip_type)  # 进入舞步模式
            self.dance_flag = 1
        else:
            self.uapi.remote_fly_entry_remote_mode(self.equip_type)  # 进入遥控模式
            self.remote_flag = 1

        # 监听是否需要紧急降落
        self.emergency_landing_thread = threading.Thread(target=self._emergency_landing_thread)
        self.emergency_landing_thread.daemon = True
        self.emergency_landing_thread.start()

    def _emergency_landing_thread(self):
        with Listener(on_press=self.emergency_landing) as listener:
            listener.join()

    def emergency_landing(self, key):
        """按键监听，紧急降落"""
        if key == Key.esc:  # 紧急降落
            print("dance thread stop")
            if self.dance_flag:
                self.uapi.dance_fly_touchdown(True, self.equip_type)
            if self.remote_flag:
                self.uapi.remote_fly_touchdown_remote(True, self.equip_type)
            # os._exit(0)
            sys.exit()

    def takeoff(self, block=True):
        """起飞"""
        if self.dance_flag:
            return self.uapi.dance_fly_takeoff(block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_takeoff_remote(self.equip_type)
        time.sleep(2)

    def land(self, block=True):
        """降落"""
        if self.dance_flag:
            return self.uapi.dance_fly_touchdown(block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_takeoff_remote(self.equip_type)

    def forward(self, distance, speed=500, block=True):
        """前进"""
        if self.dance_flag:
            return self.uapi.dance_fly_forward(distance, speed, block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_forward_remote(speed, self.equip_type)

    def back(self, distance, speed=500, block=True):
        """后退"""
        if self.dance_flag:
            return self.uapi.dance_fly_back(distance, speed, block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_back_remote(speed, self.equip_type)

    def left(self, distance, speed=500, block=True):
        """左平移"""
        if self.dance_flag:
            return self.uapi.dance_fly_left(distance, speed, block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_left_remote(speed, self.equip_type)

    def right(self, distance, speed=500, block=True):
        """右平移"""
        if self.dance_flag:
            return self.uapi.dance_fly_right(distance, speed, block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_right_remote(speed, self.equip_type)

    def up(self, height, speed=500, block=True):
        """上升"""
        if self.dance_flag:
            return self.uapi.dance_fly_up(height, speed, block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_up_remote(speed, self.equip_type)

    def down(self, height, speed=500, block=True):
        """下降"""
        if self.dance_flag:
            return self.uapi.dance_fly_down(height, speed, block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_down_remote(speed, self.equip_type)

    def turn_left(self, angle=90, speed=500, block=True):
        """左转"""
        if self.dance_flag:
            return self.uapi.dance_fly_turnleft(angle, block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_turnleft_remote(speed, self.equip_type)

    def turn_right(self, angle=90, speed=500, block=True):
        """右转"""
        if self.dance_flag:
            return self.uapi.dance_fly_turnright(angle, block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_turnright_remote(speed, self.equip_type)

    def flip_forward(self, block=True):
        """向前翻滚"""
        if self.dance_flag:
            return self.uapi.dance_fly_flip_forward(block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_flip_forward_remote(self.equip_type)

    def flip_back(self, block=True):
        """向后翻滚"""
        if self.dance_flag:
            return self.uapi.dance_fly_flip_back(block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_flip_back_remote(self.equip_type)

    def flip_left(self, block=True):
        """向左翻滚"""
        if self.dance_flag:
            return self.uapi.dance_fly_flip_left(block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_flip_left_remote(self.equip_type)

    def flip_right(self, block=True):
        """向右翻滚"""
        if self.dance_flag:
            return self.uapi.dance_fly_flip_right(block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_flip_right_remote(self.equip_type)

    def wait(self, wait_time, block=True):
        """悬停"""
        if self.dance_flag:
            return self.uapi.dance_fly_wait(wait_time, block, self.equip_type)
        if self.remote_flag:
            return self.uapi.remote_fly_remote(0, 0, 0, 0, self.equip_type)

    #  ======================================仅在 dance 模式下可用的方法====================================================

    def left_rounds(self, rounds, block=True):
        """飞机向左转圈"""
        self.uapi.dance_fly_turnleftrounds(rounds, block, self.equip_type)

    def righ_trounds(self, rounds, block=True):
        """飞机向右转圈"""
        self.uapi.dance_fly_turnrightrounds(rounds, block, self.equip_type)

    def bounce(self, times, block=True):
        """飞机进入弹跳模式"""
        self.uapi.dance_fly_bounce(times, block, self.equip_type)

    def surround(self, radius, block=True):
        """飞机环绕飞行"""
        self.uapi.dance_fly_surround(radius, block, self.equip_type)

    def straight_flight(self, x, y, z, speed=500, block=True):
        """飞机直线移动，(x,y,z)是从当前位置到目标位置的位移"""
        self.uapi.dance_fly_straight_flight(x, y, z, speed, block, self.equip_type)

    def curve_flight_clockwise(self, x, y, z, speed=500, block=True):
        """飞机按照椭圆的方式顺时针方向曲线飞行，(x,y,z)是从当前位置到目标位置的位移"""
        self.uapi.dance_fly_curve_flight_clockwise(x, y, z, speed, block, self.equip_type)

    def curve_flight_anticlockwise(self, x, y, z, speed=500, block=True):
        """飞机按照椭圆的方式逆时针方向曲线飞行，(x,y,z)是从当前位置到目标位置的位移"""
        self.uapi.dance_fly_curve_flight_anticlockwise(x, y, z, speed, block, self.equip_type)

    #  ======================================仅在 remote 模式下可用的方法===================================================

    def remote_fly(self, pitch, roll, yaw, accelerator):
        """遥控器模式控制飞行方向， pitch:俯仰   roll:横滚   yaw:航向   accelerator:油门，-1000 < 值 < 1000"""
        self.uapi.remote_fly_remote(pitch, roll, yaw, accelerator, self.equip_type)

    #  ============================================获取飞机状态的方法=======================================================

    def get_battery(self):
        """获取飞机电量"""
        return self.uapi.get_battery(self.equip_type)

    def get_attitude(self):
        """获取飞机姿态"""
        return self.uapi.get_attitude(self.equip_type)

    def get_coordinate(self):
        """获取飞机坐标"""
        return self.uapi.get_coordinate(self.equip_type)

    def get_speed(self):
        """获取飞机速度"""
        return self.uapi.get_speed(self.equip_type)

    def get_accelerated(self):
        """获取飞机加速度"""
        return self.uapi.get_accelerated_speed(self.equip_type)

    def get_sensor(self):
        """获取飞机传感器健康状态"""
        return self.uapi.get_sensor_is_healthly(self.equip_type)

    def get_version(self):
        """获取飞机版本号"""
        return self.uapi.get_version(self.equip_type)

    def extend_get_data(self):
        """拓展接口"""
        return self.uapi.extend_get_data()

    def show_plane_sensor(self, id_drone=0):
        """打印输出飞机传感器健康状态"""
        return self.uapi.show_plane_sensor(self.equip_type, id_drone)

    def show_plane(self):
        """获取飞机所有状态"""
        print('================', self.equip_type, '================')
        print('Battery: ', self.uapi.get_battery(self.equip_type))
        print('Sensor Health: ', self.uapi.get_sensor_is_healthly(self.equip_type))
        _att = self.uapi.get_attitude(self.equip_type)
        print('yaw: ', _att[0], ' pitch: ', _att[1], ' roll: ', _att[2])
        _coordinate = self.uapi.get_coordinate(self.equip_type)
        print('x: ', _coordinate[0], ' y: ', _coordinate[1], ' z: ', _coordinate[2])
        _speed = self.uapi.get_speed(self.equip_type)
        print('speed x: ', _speed[0], ' speed y: ', _speed[1], ' speed z: ', _speed[2])
        _acc_speed = self.uapi.get_accelerated_speed(self.equip_type)
        print('acc speed x: ', _acc_speed[0], ' acc speed y: ', _acc_speed[1], ' acc speed z: ', _acc_speed[2])
        print('=====================================================')

    #  =============================================控制摄像头的方法========================================================

    def camera_take_photo(self):
        """拍照，照片存储在摄像头的sd卡上"""
        return self.uapi.camera_take_photo()

    def camera_on(self):
        """开始录像，视频存储在摄像头的sd卡上"""
        return self.uapi.camera_take_video_on()

    def camera_off(self):
        """停止录像，视频存储在摄像头的sd卡上"""
        return self.uapi.camera_take_video_off()

    def camera_status(self):
        """获取SD卡录像状态"""
        return self.uapi.camera_get_take_video_status()

    #  =============================================控制视频流的方法========================================================

    def stream_on(self):
        """开始获取视频流"""
        return self.uapi.stream_on()

    def stream_off(self):
        """停止获取视频流"""
        return self.uapi.stream_off()

    def stream_show(self):
        """实时显示视频流"""
        return self.uapi.stream_show()

    def stream_stop(self):
        """停止显示视频流"""
        return self.uapi.stream_stop_show()

    def stream_flip(self, flip):
        """水平反转视频流"""
        return self.uapi.stream_flip(flip)

    def stream_set_path(self, path=os.getcwd()):
        """设置照片和视频的存储路径"""
        return self.uapi.stream_set_path(path)

    def stream_take_photo(self):
        """拍一张照片，存储在stream_set_path设置的路径上"""
        return self.uapi.stream_take_photo()

    def stream_take_video_on(self):
        """开始录像，视频存储在stream_set_path设置的路径上"""
        return self.uapi.stream_take_video_on()

    def stream_take_video_off(self):
        """停止录像，视频存储在stream_set_path设置的路径上"""
        return self.uapi.stream_take_video_off()

    def stream_get_status(self):
        """获取视频流运行状态"""
        return self.uapi.stream_get_status()

    def stream_show_tatus(self):
        """获取视频流显示状态"""
        return self.uapi.stream_get_stream_show_status()

    def stream_video_status(self):
        """获取录像状态"""
        return self.uapi.stream_get_take_video_status()

    def stream_get_frame(self):
        """返回一帧图像"""
        return self.uapi.stream_get_frame()

    def stream_get_height(self):
        """获取视频分辨率的高度信息"""
        return self.uapi.stream_get_height()

    def stream_get_width(self):
        """获取视频分辨率的宽度信息"""
        return self.uapi.stream_get_width()

    def stream_get_fps(self):
        """获取视频帧率"""
        return self.uapi.stream_get_fps()

    def stream_draw_rectangle(self, rectangle_id, start_x, start_y, end_x, end_y, r, g, b, thickness):
        """
            在视频流上画框
            rectangle_id: 边框的编号
            start_x: 画框的左上角x坐标
            start_y: 画框的左上角y坐标
            end_x: 画框右下角x坐标
            end_y: 画框的右下角y坐标
            r: 设置画框红色色值(0 - 255)
            g: 设置画框绿色色值(0 - 255)
            b: 设置画框蓝色色值(0 - 255)
            thickness: 画框厚度(0 - 20)
        """
        return self.uapi.stream_draw_rectangle(rectangle_id, start_x, start_y, end_x, end_y, r, g, b, thickness)

    def stream_draw_rectangle_mouse(self, rectangle_id, r, g, b, thickness, ret=0):
        """
            在视频流上使用鼠标画框
            rectangle_id: 画框的编号
            r: 设置画框红色色值(0-255)
            g: 设置画框绿色色值(0-255)
            b: 设置画框蓝色色值(0-255)
            thickness: 画框厚度(0-20)
            ret: 是否返回坐标，1为返回，0为不返回。当需要返回坐标时该函数会阻塞。
        """
        return self.uapi.stream_draw_rectangle_by_mouse(rectangle_id, r, g, b, thickness, ret)

    def stream_clear_rectangle(self, rectangle_id=None):
        """删除视频流上的画框"""
        # 画完一个画框后，画框会在下一帧的图像上开始显示。
        # 如果调用stream_draw_rectangle或者stream_draw_rectangle_by_mouse后
        # 立即调用stream_clear_rectangle，那么画框很可能没显示出来
        return self.uapi.stream_clear_rectangle(rectangle_id)

    def stream_draw_text(self, text_id, string, x, y, size, r, g, b):
        """
            在视频流上显示文字(目前只能正常显示英文)
            text_id: 文字的编号
            string: 显示的内容
            x: 文字放置的坐标x
            y: 文字放置的坐标y
            size: 字体大小（0-5）
            r: 设置边框红色色值(0-255)
            g: 设置边框绿色色值(0-255)
            b: 设置边框蓝色色值(0-255)
        """
        return self.uapi.stream_draw_text(text_id, string, x, y, size, r, g, b)

    def stream_clear_text(self, text_id=None):
        """删除在视频流上显示的文字，text_id:文字的编号, 当text_id为None时清除所有文字"""
        return self.uapi.stream_clear_text(text_id)

    #  =============================================控制LED灯带的方法=======================================================

    def get_led(self, led_id):
        """
            获取飞机灯带灯光样式，led_id: 灯光编号（0-5）
            返回值
                []:参数错误
                [r, g, b, delay, mode, send]:获取灯光当前样式状态成功
                r:红色灯亮度(延时模式:0-255 三色灯模式:0)
                g:绿色灯亮度(延时模式:0-255 三色灯模式:0)
                b:蓝色灯亮度(延时模式:0-255 三色灯模式:0)
                delay:剩余时长(ms)
                mode:灯光模式(延时模式:0 三色灯模式:1)
                send:灯光样式是否已经提交。
                使用led_set_sync设置灯光样式后灯光样式处于未提交状态，调用led_set_sync_confirm后灯光样式才会提交(未提交:0, 已提交:1)
        """
        return self.uapi.led_get(led_id)

    def set_led(self, led_id, mode, delay, r, g, b):
        """
            设置灯光样式
            led_id: 灯光编号（0-5）
            mode: 灯光模式（填0）
            delay: 时长(0-50000ms)
            r: 灯光红色色值(0-255)
            g: 灯光绿色色值(0-255)
            b: 灯光蓝色色值(0-255)
        """
        return self.uapi.led_set(led_id, mode, delay, r, g, b)

    def set_led_sync(self, led_id, mode, delay, r, g, b):
        """
            同时设置灯光样式。调用该函数后灯光样式不会立即改变，需要调用led_set_sync_confirm提交灯光样式。
            连续使用led_set设置灯光时，无法保证灯光样式是同时配置的。使用该函数可以确保灯光样式是同时配置的。
            led_id: 灯光编号（0-5）
            mode: 灯光模式（填0）
            delay: 时长(0-50000ms)
            r: 灯光红色色值(0-255)
            g: 灯光绿色色值(0-255)
            b: 灯光蓝色色值(0-255)
        """
        return self.uapi.led_set_sync(led_id, mode, delay, r, g, b)

    def set_led_sync_confirm(self):
        """提交灯光样式"""
        return self.uapi.led_set_sync_confirm()

    def set_led_front(self, left_color, right_color, mode, delay, led_id=0):
        """
            飞机头部灯光设置
            left_color: 左灯颜色('red', 'green', 'black')
            right_color: 右灯颜色('red', 'green', 'black')
            mode: 灯光模式（填1）
            delay: 灯光时长(ms)
            equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
            led_id: 无人机编号，不填时默认为0
        """
        return self.uapi.led_set_front_color(left_color, right_color, mode, delay, self.equip_type, led_id)

    #  ===============================================AI的控制方法==========================================================

    def ai_target_detect(self, frame=None, width=-1, height=-1):
        """
            目标识别
            可识别: aeroplane、bicycle、bird、boat、bottle、bus、car、cat、chair、cow、diningtable、dog、horse、
                    motorbike、person、pottedplant、sheep、sofa、train、tvmonitor
            frame: 需要识别的图像，如果frame为None，并且视频流已经启动，则自动获取最新的一帧填入
            width: 图像的宽度，如果frame为None,width可不填
            height: 图像的高度，如果frame为None,height可不填
        """
        return self.uapi.ai_target_detect(frame, width, height)

    def ai_gesture_detect(self, frame=None, width=-1, height=-1):
        """
            手势识别，可识别 hand和fist
            frame: 需要识别的图像，如果frame为None，并且视频流已经启动，则自动获取最新的一帧填入
            width: 图像的高度，如果frame为None,width可不填
            height: 图像的宽度，如果frame为None,height可不填
        """
        return self.uapi.ai_gesture_detect(frame, width, height)

    def ai_tracker_on(self, start_x, start_y, end_x, end_y, rectangle_id=None):
        """
            开始跟踪画框框出的目标，跟踪画框的大小不能小于50x50
            start_x: 画框的左上角x坐标
            start_y: 画框的左上角y坐标
            end_x: 画框的右下角x坐标
            end_y: 画框的右下角y坐标
            rectangle_id: 画框id号,当该参数被填入时,之前的四个坐标会被忽略,同时会自动更新画框的位置
        """
        return self.uapi.ai_tracker_on(start_x, start_y, end_x, end_y, rectangle_id)

    def ai_tracker_off(self):
        """停止目标跟踪"""
        return self.uapi.ai_tracker_off()

    def ai_tracker_get_target(self):
        """获取跟踪目标的坐标"""
        return self.uapi.ai_tracker_get_target()

    def ai_code_detect(self, frame=None, width=-1, height=-1):
        """二维码识别，可识别Folk定制的二维码"""
        return self.uapi.ai_qrcode_detect(frame, width, height)

    #  ==============================================无人机系统设置=========================================================

    def equipment_create(self):
        """创建无人机设备"""
        return self.uapi.equipment_create(self.equip_type)

    def equipment_remove(self, drone_id=0):
        """删除无人机设备"""
        return self.uapi.equipment_remove(self.equip_type, drone_id)

    def equipment_show(self):
        """打印输出所有无人机设备的类型和id"""
        return self.uapi.equipment_show()

    def plane_connect(self, drone_id=0):
        """连接到无人机设备"""
        return self.uapi.plane_connect(self.equip_type, drone_id)

    def plane_disconnect(self, drone_id=0):
        """断开与无人机设备的连接"""
        return self.uapi.plane_disconnect(self.equip_type, drone_id)

    def plane_get_connect_state(self, drone_id=0):
        """获取飞机连接状态"""
        return self.uapi.plane_get_connect_state(self.equip_type, drone_id)

    def reset_wifi(self, ss_id, password, drone_id=0):
        """
            重置wifi名称与wifi密码
            ss_id: wifi名称
            password: wifi密码
        """
        return self.uapi.plane_sys_reset_wifi(ss_id, password, self.equip_type, drone_id)

    def update_firmware(self, firmware_path, drone_id=0):
        """
            更新飞机固件, firmware_path: 固件路径
            升级飞机固件时，最好连接飞机wifi，不要连接摄像头wifi，以保证升级成功率
        """
        return self.uapi.plane_sys_update_firmware(firmware_path, self.equip_type, drone_id)

    def get_firmware_update_rate(self, drone_id=0):
        """获取固件上传进度,用户接口都是串行处理，如果需要获取进度，则需要在线程中调用该函数进行获取"""
        return self.uapi.plane_sys_get_firmware_update_rate(self.equip_type, drone_id)

    # ==============================================飞机锁得控制方法========================================================

    def single_fly_arm(self, drone_id=0):
        """飞机解锁"""
        return self.uapi.single_fly_arm(self.equip_type, drone_id)

    def single_fly_disarm(self, equipment_type, drone_id=0):
        """飞机上锁，紧急停桨"""
        return self.uapi.single_fly_disarm(equipment_type, drone_id)
