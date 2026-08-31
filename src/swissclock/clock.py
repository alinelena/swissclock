# SPDX-License-Identifier: GPL-3.0-or-later
import sys
import math
from PySide6.QtCore import Qt, QTime, QRectF
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import QApplication
from .base_dial import BaseDial

class AnalogClock(BaseDial):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analog Clock")
        self.resize(300, 300)

    def draw_face(self, painter):
        # Draw 24 hour markers (thick lines for even, red dots for odd)
        painter.save()
        for i in range(24):
            if i % 2 == 0:
                painter.setBrush(self.black_color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QRectF(83, -4, 8, 8))
            else:
                painter.setBrush(self.red_color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QRectF(85, -2, 4, 4))
            painter.rotate(15.0)
        painter.restore()

        # Draw 60 minute markers (small black circles)
        painter.save()
        painter.setBrush(self.black_color)
        painter.setPen(Qt.NoPen)
        for i in range(60):
            painter.drawEllipse(QRectF(85, -2, 4, 4))
            painter.rotate(6.0)
        painter.restore()

        # Draw numbers (even inside, odd outside)
        painter.save()
        font = painter.font()
        font.setFamily("Verdana")
        font.setPointSize(6)
        font.setBold(True)
        painter.setFont(font)
        
        window_text_color = self.palette().windowText().color()
        
        for h in range(1, 25):
            angle_deg = -90 + h * 15
            angle_rad = math.radians(angle_deg)
            if h % 2 == 0:
                x = 65 * math.cos(angle_rad)
                y = 65 * math.sin(angle_rad)
                painter.setPen(self.black_color)
            else:
                x = 108 * math.cos(angle_rad)
                y = 108 * math.sin(angle_rad)
                painter.setPen(window_text_color)
            
            rect = QRectF(x - 10, y - 10, 20, 20)
            painter.drawText(rect, Qt.AlignCenter, str(h))
        painter.restore()

        # Draw minute labels outside the clock
        painter.save()
        font = painter.font()
        font.setFamily("Courier New")
        font.setPointSize(4)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(self.palette().windowText().color())
        for m in range(0, 60, 5):
            angle_deg = -90 + m * 6
            angle_rad = math.radians(angle_deg)
            x = 108 * math.cos(angle_rad)
            y = 108 * math.sin(angle_rad)
            rect = QRectF(x - 10, y - 10, 20, 20)
            painter.drawText(rect, Qt.AlignCenter, f"{m:02d}")
        painter.restore()

    def draw_hands(self, painter):
        time = QTime.currentTime()
        
        # Hour hand
        hour_angle = 15.0 * (time.hour() + time.minute() / 60.0 + time.second() / 3600.0)
        self.draw_capsule_hand(painter, hour_angle, self.black_color, (-4, -55, 8, 70, 4.0, 4.0))

        # Minute hand (Swiss clocks jump the minute hand at the exact minute)
        minute_angle = 6.0 * time.minute()
        self.draw_capsule_hand(painter, minute_angle, self.black_color, (-3, -75, 6, 95, 3.0, 3.0))

        # Second hand (waits for 1.5s at 60, then jumps directly to 1.5 seconds)
        ms = time.second() * 1000 + time.msec()
        if ms < 1500:
            second_angle = 0.0
        else:
            second_angle = ms * (360.0 / 60000.0)

        self.draw_swiss_second_hand(painter, second_angle)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = AnalogClock()
    clock.show()
    sys.exit(app.exec())
