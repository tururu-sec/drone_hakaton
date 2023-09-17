from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QTransform, QBrush, QColor
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem


class JoystickDisplay(QGraphicsView):
    viewUpdate = pyqtSignal();

    def __init__(self, winParent):
        QGraphicsView.__init__(self)

        self.winParent = winParent

        self.viewUpdate.connect(self.update)

        self.m_roll = 0.0
        self.m_pitch = 0.0
        self.m_yaw = 0.0
        self.m_thr = 0.0

        self.m_stick1X_new = 0
        self.m_stick1Y_new = 0
        self.m_stick2X_new = 0
        self.m_stick2Y_new = 0
        self.m_stick1X_old = 0
        self.m_stick1Y_old = 0
        self.m_stick2X_old = 0
        self.m_stick2Y_old = 0

        self.m_backZ = -10
        self.m_sticksZ = 10

        self.setStyleSheet('background: transparent; border:none')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setInteractive(False)
        self.setEnabled(False)

        self.m_scene = QGraphicsScene(self)
        self.setScene(self.m_scene)

        self.init()

    def init(self):
        self.m_itemBack = QGraphicsSvgItem('controller_back.svg')
        self.m_itemBack.setCacheMode(QGraphicsItem.NoCache)
        self.m_itemBack.setZValue(self.m_backZ)
        self.m_scene.addItem(self.m_itemBack)

        self.m_itemStick1 = QGraphicsEllipseItem(50, 0, 20, 20)
        b = QBrush(Qt.red)
        self.m_itemStick1.setBrush(b)
        self.m_itemStick1.setCacheMode(QGraphicsItem.NoCache)
        self.m_itemStick1.setZValue(self.m_sticksZ)
        self.m_scene.addItem(self.m_itemStick1)

    def reinit(self):
        if(self.m_scene):
            self.m_scene.clear()
            self.init()

    def update(self):
        self.updateView()
        self.m_stick1X_old = self.m_stick1X_new
        self.m_stick1Y_old = self.m_stick1X_new
        self.m_stick2X_old = self.m_stick2X_new
        self.m_stick2Y_old = self.m_stick2Y_new

    def setValues(self, channels):
        self.m_roll = min(max(channels[0], -1.0), 1.0)
        self.m_pitch = min(max(channels[1], -1.0), 1.0)
        self.m_yaw = min(max(channels[2], -1.0), 1.0)
        self.m_thr = min(max(channels[3], -1.0), 1.0)

    def resizeEvent(self, event):
        QGraphicsView.resizeEvent(self, event)
        self.reinit()

    def reset(self):
        self.m_itemBack = None
        self.m_itemStick1 = None

        self.m_roll = 0.0
        self.m_pitch = 0.0
        self.m_yaw = 0.0
        self.m_thr = 0.0

    #def updateView(self):
