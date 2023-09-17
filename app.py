import sys

import folium
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QGraphicsView, QComboBox, QPushButton, QLCDNumber, QSlider
from serial.tools import list_ports

from JoystickDisplay import JoystickDisplay
from qfi.qfi_ADI import qfi_ADI


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)

        self.portsList = []

        self.UAV_attitude = (0.0, 0.0, 0.0)
        self.UAV_altitude = 0.0
        self.UAV_speed = 0.0
        self.UAV_batt_vol = 0.0
        self.UAV_batt_cur = 0.0
        self.UAV_sat_num = 0
        self.UAV_pos = (0.0, 0.0)
        self.p_UAV_pos = (0.0, 0.0)

        self.RC_cmd = (1500, 1500, 1000, 1500) # This is being sent to FC
        self.UAV_rc = (1500, 1500, 1000, 1500) # This is being read from FC

        w = self.findChild(QGraphicsView, 'ADI_placeholder')
        l = w.parent().layout()
        self.ADI = qfi_ADI(l)
        l.replaceWidget(w, self.ADI)
        w.setParent(None)

        self.portSelectionBox = self.findChild(QComboBox, 'portSelection')
        self.connectButton = self.findChild(QPushButton, 'connectButton')
        self.mapDisplay = self.findChild(QWebEngineView, 'MapView')

        self.altitudeDisplay = self.findChild(QLCDNumber, 'alt_disp')
        self.speedDisplay = self.findChild(QLCDNumber, 'spd_disp')
        self.headingDisplay = self.findChild(QLCDNumber, 'hdg_disp')
        self.voltageDisplay = self.findChild(QLCDNumber, 'volt_disp')
        self.currentDisplay = self.findChild(QLCDNumber, 'curr_disp')
        self.satelliteNumberDisplay = self.findChild(QLCDNumber, 'sat_disp')

        self.rcRateSlider = self.findChild(QSlider, 'rateSlider')

        w = self.findChild(QGraphicsView, 'JoystickRender')
        l = w.parent().layout()
        self.controllerDisplay = JoystickDisplay(l)
        l.replaceWidget(w, self.controllerDisplay)
        w.setParent(None)

        self.enableRCButton = self.findChild(QPushButton, 'enableCtrlButton')

        self.updateSerialPortList()

        m = folium.Map(
            title='Map View',
            zoom_start=3,
            location=self.UAV_pos,
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            attributionControl=False
        )
        folium.Marker(location=self.UAV_pos).add_to(m)
        self.mapDisplay.setHtml(m.get_root().render())

        self.show()

        self.mapUpdateTimer = QTimer()
        self.telemetryUpdateTimer = QTimer()
        self.remoteControlUpdateTimer = QTimer()
        self.serialListUpdateTimer = QTimer()

        self.mapUpdateTimer.timeout.connect(self.updateMap)
        self.telemetryUpdateTimer.timeout.connect(self.updateTelemetry)
        self.remoteControlUpdateTimer.timeout.connect(self.updateRemoteControl)
        self.serialListUpdateTimer.timeout.connect(self.updateSerialPortList)

        self.mapUpdateTimer.start(2000)
        self.telemetryUpdateTimer.start(100)
        self.serialListUpdateTimer.start(2000)

    def updateMap(self):
        if abs(self.UAV_pos[0] - self.p_UAV_pos[0]) < 0.000001 and abs(self.UAV_pos[1] - self.p_UAV_pos[1]) < 0.000001:
            return
        self.p_UAV_pos = self.UAV_pos

        m = folium.Map(
            title='Map View',
            zoom_start=14,
            location=self.UAVPos,
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            attributionControl=False
        )
        folium.Marker(location=self.UAV_pos).add_to(m)
        self.mapDisplay.setHtml(m.get_root().render())

    def updateTelemetry(self):
        self.UAV_attitude = (0.0, 0.0, 0.0)
        self.UAV_altitude = 0.0
        self.UAV_speed = 0.0
        self.UAV_batt_vol = 0.0
        self.UAV_batt_cur = 0.0
        self.UAV_sat_num = 0
        self.UAV_pos = (0.0, 0.0)
        self.UAV_rc = (1500, 1500, 1000, 1500) # read from MSP

        self.ADI.setRoll(self.UAV_attitude[0])
        self.ADI.setPitch(self.UAV_attitude[1])
        self.ADI.update()

        self.altitudeDisplay.value = self.UAV_altitude
        self.speedDisplay.value = self.UAV_speed
        self.headingDisplay.value = self.UAV_attitude[2]
        self.voltageDisplay.value = self.UAV_batt_vol
        self.currentDisplay.value = self.UAV_batt_cur

    def updateRemoteControl(self):
        # send rc values to MSP
        pass

    def updateSerialPortList(self):
        self.portsList = (i.device for i in list_ports.comports())
        self.portSelectionBox.addItems(self.portsList)


app = QtWidgets.QApplication(sys.argv)
mainWindow = MainWindow()
sys.exit(app.exec_())
