import os

import cv2
import sys

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QAction

from look import Ui_LookAtYou
from Mytool import tool
import time


class CamShow(QMainWindow, Ui_LookAtYou):
    def __init__(self, parent=None):
        super(CamShow, self).__init__(parent)

        self.out = None
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.cap1 = cv2.VideoCapture()  # 视频流
        self.cap2 = cv2.VideoCapture()
        self.CAM_NUM1 = '1.mp4'  # 为0时表示视频流来自笔记本内置摄像头
        self.CAM_NUM2 = 0
        self.out = cv2.VideoWriter

        self.setupUi(self)  # 初始化界面
        self.slot_init()  # 初始化槽函数

    def slot_init(self):
        self.start.clicked.connect(
            self.start_clicked)  # 若该按键被点击，则调用start_clicked()

        self.outputdesktop.triggered.connect(self.OutPutDesktop)
        self.outputhere.triggered.connect(self.OutPutHere)

        self.timer_camera.timeout.connect(
            lambda: self.show_camera(self.video, self.cap1))  # self.show_camera  # 若定时器结束，则调用show_camera(?)
        self.timer_camera.timeout.connect(
            lambda: self.save_camera(self.video_2, self.cap2))
        self.exit.clicked.connect(self.close)  # 若该按键被点击，则调用close()

    '''槽函数之一'''

    def start_clicked(self):
        if not self.timer_camera.isActive():  # 若定时器未启动
            self.cap1.open(self.CAM_NUM1)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            self.cap2.open(self.CAM_NUM2)

            self.video_warning(self.video)  # 让视频边框变红
            self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
            self.out = self.SaveVideo(self.cap2)
            self.start.setText('关闭')
        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap1.release()  # 释放视频流
            self.out.release()
            self.cap2.release()
            self.video_safety(self.video)  # 让视频边框变回正常
            self.video.clear()  # 清空视频显示区域
            self.video_2.clear()
            self.start.setText('开始')

    def show_camera(self, Video: QLabel, cap):  # video参数可以放不同的窗口界面，cap参数是不同的视频流
        flag, self.image = cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (640, 480))  # 把读到的帧的大小重新设置为 640x480
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        Video.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def save_camera(self, Video: QLabel, cap):  # video参数可以放不同的窗口界面，cap参数是不同的视频流
        flag, self.image = cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (640, 480))  # 把读到的帧的大小重新设置为 640x480
        self.out.write(show)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        Video.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def video_warning(self, Video: QLabel):  # video参数可以放不同的窗口界面
        Video.setFrameShape(QFrame.Box)  # 设置阴影 只有加了这步才能设置边框颜色
        # 可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        Video.setFrameShadow(QFrame.Raised)
        # 设置线条宽度
        Video.setLineWidth(5)
        # 设置背景颜色，包括边框颜色
        Video.setStyleSheet('background-color: rgb(255, 0, 0)')

    def video_safety(self, Video: QLabel):
        Video.setFrameShape(QFrame.Box)  # 设置阴影 只有加了这步才能设置边框颜色
        # 可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        Video.setFrameShadow(QFrame.Raised)
        # 设置线条宽度
        Video.setLineWidth(5)
        # 设置背景颜色，包括边框颜色
        Video.setStyleSheet('background-color: rgb(0, 0, 0)')

    def OutPutDesktop(self):  # 将日志输出到桌面
        out = open(tool.get_desktop() + '\output.txt', 'a')
        localtime = time.asctime(time.localtime(time.time()))
        print('flame!!!' + '  ' + localtime, file=out)
        out.close()

    def OutPutHere(self):  # 将日志输出到桌面
        out = open(os.getcwd() + '\output.txt', 'a')
        localtime = time.asctime(time.localtime(time.time()))
        print('flame!!!' + '  ' + localtime, file=out)
        out.close()

    def SaveVideo(self, cap):
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        fps = cap.get(cv2.CAP_PROP_FPS)  # 帧率
        # 视频的宽高
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), \
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        return cv2.VideoWriter('INPUT_VIDEO.mp4', fourcc, fps, size)  # 视频存储


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CamShow()
    ui.show()
    sys.exit(app.exec_())
