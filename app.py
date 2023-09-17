import sys

import folium
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QGraphicsView, QComboBox, QPushButton, QLCDNumber, QSlider
from PyQt5.uic.properties import QtCore
from serial.tools import list_ports

from JoystickDisplay import JoystickDisplay
from MSP import MSP
from qfi.qfi_ADI import qfi_ADI


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)

        self.portsList = []
        self.MSP = None

        self.UAV_attitude = (0.0, 0.0, 0.0)
        self.UAV_altitude = 0.0
        self.UAV_speed = 0.0
        self.UAV_batt_vol = 0.0
        self.UAV_batt_cur = 0.0
        self.UAV_sat_num = 0
        self.UAV_pos = (0.0, 0.0)
        self.p_UAV_pos = (0.0, 0.0)

        self.RC_cmd = [1500, 1500, 1000, 1500, 1000] # This is being sent to FC
        self.UAV_rc = [1500, 1500, 1000, 1500, 1000] # This is being read from FC

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

        self.connectButton.toggled.connect(self.handleConnectButton)
        self.enableRCButton.toggled.connect(self.handleRCButton)

        self.mapUpdateTimer = QTimer()
        self.telemetryUpdateTimer = QTimer()
        self.remoteControlUpdateTimer = QTimer()
        self.serialListUpdateTimer = QTimer()

        self.mapUpdateTimer.timeout.connect(self.updateMap)
        self.telemetryUpdateTimer.timeout.connect(self.updateTelemetry)
        self.remoteControlUpdateTimer.timeout.connect(self.updateRemoteControl)
        self.serialListUpdateTimer.timeout.connect(self.updateSerialPortList)

        self.mapUpdateTimer.start(2000)
        self.telemetryUpdateTimer.start(200)
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
        if self.MSP == None:
            return
        if not self.MSP.port.isOpen():
            return

        att = self.MSP.readAttitude()
        if att is not None:
            self.UAV_attitude = att
        self.UAV_altitude = 0.0
        self.UAV_speed = 0.0
        self.UAV_batt_vol = 0.0
        self.UAV_batt_cur = 0.0
        rawGPS = self.MSP.readGPS()
        if rawGPS is not None:
            self.UAV_sat_num = rawGPS[1]
            self.UAV_pos = (rawGPS[2], rawGPS[3])
        rc_data = self.MSP.readRawRC()
        if rc_data is not None and rc_data:
            self.UAV_rc = (rc_data[0], rc_data[1], rc_data[2], rc_data[3], rc_data[4]) # read from MSP

        self.ADI.setRoll(self.UAV_attitude[0])
        self.ADI.setPitch(self.UAV_attitude[1])
        self.ADI.update()

        self.altitudeDisplay.value = self.UAV_altitude
        self.speedDisplay.value = self.UAV_speed
        self.headingDisplay.value = self.UAV_attitude[2]
        self.voltageDisplay.value = self.UAV_batt_vol
        self.currentDisplay.value = self.UAV_batt_cur

    def updateRemoteControl(self):
        self.MSP.sendRawRC(self.RC_cmd)
        pass

    def updateSerialPortList(self):
        self.portsList = (i.device for i in list_ports.comports())
        self.portSelectionBox.addItems(self.portsList)

    def handleConnectButton(self):
        if self.connectButton.isChecked():
            self.MSP = MSP('COM8')
        else:
            self.MSP.port.close()

    def handleRCButton(self):
        if self.enableRCButton.isChecked():
            self.RC_cmd[2] = 1000
            self.RC_cmd[4] = 2000
            self.remoteControlUpdateTimer.start(100)
        else:
            self.remoteControlUpdateTimer.stop()
            self.RC_cmd[4] = 1000
            self.MSP.sendRawRC(self.RC_cmd)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.RC_cmd[0] = 1500 + self.rcRateSlider.value()
        elif event.key() == Qt.Key_S:
            self.RC_cmd[0] = 1500 - self.rcRateSlider.value()

        if event.key() == Qt.Key_A:
            self.RC_cmd[1] = 1500 + self.rcRateSlider.value()
        elif event.key() == Qt.Key_D:
            self.RC_cmd[1] = 1500 - self.rcRateSlider.value()

        if event.key() == Qt.Key_Q:
            self.RC_cmd[3] = 1500 + self.rcRateSlider.value()
        elif event.key() == Qt.Key_E:
            self.RC_cmd[3] = 1500 - self.rcRateSlider.value()

        if event.key() == Qt.Key_Shift:
            self.RC_cmd[2] = min(self.RC_cmd[2] + 10, 2000)
        elif event.key() == Qt.Key_Control:
            self.RC_cmd[2] = max(self.RC_cmd[2] - 10, 1000)

        print(self.RC_cmd)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_W or event.key() == Qt.Key_S:
            self.RC_cmd[0] = 1500

        if event.key() == Qt.Key_A or event.key() == Qt.Key_D:
            self.RC_cmd[1] = 1500

        if event.key() == Qt.Key_Q or event.key() == Qt.Key_E:
            self.RC_cmd[3] = 1500

        print(self.RC_cmd)

app = QtWidgets.QApplication(sys.argv)
mainWindow = MainWindow()
sys.exit(app.exec_())
