import math

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QRectF, QEvent, QSize

class AttitudeIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pitch = 0
        self.setMinimumSize(200, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setPitch(self, pitch):
        self.pitch = pitch
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        centerX = self.width() / 2
        centerY = self.height() / 2

        font = painter.font()
        font.setPointSizeF(12)
        painter.setFont(font)

        pen = painter.pen()

        painter.save()
        painter.translate(centerX, centerY)
        painter.rotate(self.pitch)

        width = min(self.width(), self.height())
        radius = width / 2.5

        painter.setBrush(Qt.white)
        painter.drawEllipse(int(0), int(0), int(radius), int(radius))

        pen.setColor(Qt.black)
        pen.setWidthF(2)
        painter.setPen(pen)

        for i in range(-90, 91, 10):
            markHeight = radius * math.sin(math.radians(i))
            painter.drawLine(int(-radius), int(markHeight), int(radius), int(markHeight))

        painter.setPen(Qt.black)
        painter.drawText(QRectF(-25, -radius - 20, 50, 20), Qt.AlignCenter, "-90°")
        painter.drawText(QRectF(-25, radius, 50, 20), Qt.AlignCenter, "90°")

        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(Qt.black)
        painter.drawRect(-5, -radius - 10, 10, radius / 6)
        painter.drawPolygon([(-10, radius / 6 - 5), (10, radius / 6 - 5), (0, radius / 6 + 5)])

        painter.restore()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    mainWindow = QMainWindow()
    mainWindow.setWindowTitle("Attitude Indicator")

    attitudeWidget = AttitudeIndicator(mainWindow)
    attitudeWidget.setPitch(30) # Set initial pitch angle
    mainWindow.setCentralWidget(attitudeWidget)

    mainWindow.show()

    sys.exit(app.exec_())