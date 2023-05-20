# -*- coding:utf-8 -*-


from PyQt5.Qt import *

from gtyConfig import language, systemConfig


# 屏幕居中
def centerAndSetIcon(window):
    # 获取窗口大小
    screen = QDesktopWidget().screenGeometry()
    size = window.geometry()
    # 本窗体运动
    window.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))
    window.setWindowIcon(QIcon(systemConfig.param.windowLogoPath))
