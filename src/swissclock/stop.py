# SPDX-License-Identifier: GPL-3.0-or-later
import math
import sys

from PySide6.QtCore import QElapsedTimer, QRectF, Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QApplication, QInputDialog, QMenu

from .base_dial import BaseDial
from .morph_digit import MorphDigit


class StopWatch(BaseDial):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.running = False
        self.elapsed_timer = QElapsedTimer()
        self.total_elapsed = 0
        self.countdown_target_ms = 0
        self.is_digital = False
        
        # 5 digits for H:MM:SS
        self.digits = [MorphDigit() for _ in range(5)]

        self.setWindowTitle("Stopwatch")
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        

    def show_context_menu(self, pos):
        menu = QMenu(self)
        
        action_stopwatch = menu.addAction("Stopwatch Mode")
        action_1min = menu.addAction("1 Minute")
        action_5min = menu.addAction("5 Minutes")
        action_10min = menu.addAction("10 Minutes")
        action_custom = menu.addAction("Custom...")
        menu.addSeparator()
        action_help = menu.addAction("Help (Shortcuts)")
        action_about = menu.addAction("About")
        
        action = menu.exec(self.mapToGlobal(pos))
        
        if action == action_stopwatch:
            self.set_countdown(0)
        elif action == action_1min:
            self.set_countdown(60 * 1000)
        elif action == action_5min:
            self.set_countdown(5 * 60 * 1000)
        elif action == action_10min:
            self.set_countdown(10 * 60 * 1000)
        elif action == action_custom:
            mins, ok = QInputDialog.getInt(self, "Custom Countdown", "Enter minutes:", 1, 1, 999)
            if ok:
                self.set_countdown(mins * 60 * 1000)
        elif action == action_help:
            self.show_help()
        elif action == action_about:
            self.show_about()

    def toggle_digital_mode(self):
        self.is_digital = not self.is_digital
        self.update()

    def update_dial(self):
        if self.is_digital:
            ms = self.get_elapsed_ms()
            abs_ms = abs(ms)
            s = (abs_ms % 60000) // 1000
            m = (abs_ms % 3600000) // 60000
            h = abs_ms // 3600000
            
            self.digits[0].set_target(h % 10)
            self.digits[1].set_target(m // 10)
            self.digits[2].set_target(m % 10)
            self.digits[3].set_target(s // 10)
            self.digits[4].set_target(s % 10)
            
            for digit in self.digits:
                digit.update()
        
        super().update_dial()

    def paintEvent(self, event):
        if not self.is_digital:
            super().paintEvent(event)
            return

        ms = self.get_elapsed_ms()
        
        if self.total_elapsed == 0 and not self.running:
            color = Qt.white
        elif self.countdown_target_ms > 0:
            if ms < 0:
                color = self.red_color
            elif ms <= 0.10 * self.countdown_target_ms:
                color = self.orange_color
            else:
                color = self.green_color
        else:
            color = self.green_color

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.black)
        
        # H:MM:SS layout scaling
        digit_w = self.width() * 0.1
        digit_h = digit_w * 2.0
        gap = digit_w * 0.4
        colon_gap = digit_w * 0.8
        
        total_w = digit_w * 5 + gap * 2 + colon_gap * 2
        
        start_x = (self.width() - total_w) / 2
        start_y = (self.height() - digit_h) / 2
        
        curr_x = start_x
        
        # Draw Negative sign if in overtime
        if ms < 0:
            pen = QPen(color)
            pen.setWidthF(max(2.0, digit_w * 0.15))
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(start_x - digit_w * 0.8, start_y + digit_h / 2, start_x - digit_w * 0.2, start_y + digit_h / 2)
        
        # Draw H
        self.digits[0].draw(painter, curr_x, start_y, digit_w, digit_h / 2.0, color)
        curr_x += digit_w + colon_gap / 2
        
        # Draw Colon 1
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        radius = digit_w * 0.15
        painter.drawEllipse(curr_x - radius, start_y + digit_h * 0.35 - radius, radius*2, radius*2)
        painter.drawEllipse(curr_x - radius, start_y + digit_h * 0.65 - radius, radius*2, radius*2)
        curr_x += colon_gap / 2
        
        # Draw M1, M2
        self.digits[1].draw(painter, curr_x, start_y, digit_w, digit_h / 2.0, color)
        curr_x += digit_w + gap
        self.digits[2].draw(painter, curr_x, start_y, digit_w, digit_h / 2.0, color)
        curr_x += digit_w + colon_gap / 2
        
        # Draw Colon 2
        painter.drawEllipse(curr_x - radius, start_y + digit_h * 0.35 - radius, radius*2, radius*2)
        painter.drawEllipse(curr_x - radius, start_y + digit_h * 0.65 - radius, radius*2, radius*2)
        curr_x += colon_gap / 2
        
        # Draw S1, S2
        self.digits[3].draw(painter, curr_x, start_y, digit_w, digit_h / 2.0, color)
        curr_x += digit_w + gap
        self.digits[4].draw(painter, curr_x, start_y, digit_w, digit_h / 2.0, color)

    def draw_face(self, painter):
        # Draw 60 second markers (big for multiples of 5, small for others)
        painter.save()
        for i in range(60):
            if i % 5 == 0:
                painter.setBrush(self.black_color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QRectF(83, -4, 8, 8))
            else:
                painter.setBrush(self.black_color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QRectF(85, -2, 4, 4))
            painter.rotate(6.0)
        painter.restore()

        # Draw numbers every 1 second outside
        painter.save()
        font = painter.font()
        font.setFamily("Courier New")
        font.setPointSize(4) 
        font.setBold(True)
        painter.setFont(font)
        
        window_text_color = self.palette().windowText().color()
        painter.setPen(window_text_color)
        
        for m in range(60):
            angle_deg = -90 + m * 6
            angle_rad = math.radians(angle_deg)
            x = 108 * math.cos(angle_rad)
            y = 108 * math.sin(angle_rad)
            
            rect = QRectF(x - 10, y - 10, 20, 20)
            painter.drawText(rect, Qt.AlignCenter, f"{m:02d}")
        painter.restore()

    def draw_hands(self, painter):
        ms = self.get_elapsed_ms()
        
        # Minute hand (smooth rotation)
        minute_angle = (ms % 3600000) * (360.0 / 3600000.0)
        
        if self.total_elapsed == 0 and not self.running:
            hand_color = self.black_color
        elif self.countdown_target_ms > 0:
            if ms < 0:
                hand_color = self.red_color
            elif ms <= 0.10 * self.countdown_target_ms:
                hand_color = self.orange_color
            else:
                hand_color = self.green_color
        else:
            hand_color = self.green_color
            
        self.draw_capsule_hand(painter, minute_angle, hand_color, (-3, -75, 6, 95, 3.0, 3.0))

        # Draw second hand (Swiss railway animation: wait at top for 1.5s)
        sec_ms = ms % 60000
        
        raw_elapsed = self.total_elapsed
        if self.running:
            raw_elapsed += self.elapsed_timer.elapsed()
            
        if raw_elapsed >= 1500:
            if self.countdown_target_ms > 0:
                if sec_ms > 58500:
                    second_angle = 0.0
                else:
                    second_angle = sec_ms * (360.0 / 60000.0)
            else:
                if sec_ms < 1500:
                    second_angle = 0.0
                else:
                    second_angle = sec_ms * (360.0 / 60000.0)
        else:
            second_angle = sec_ms * (360.0 / 60000.0)

        self.draw_swiss_second_hand(painter, second_angle)

    def toggle_timer(self):
        if self.running:
            # Pause
            self.total_elapsed += self.elapsed_timer.elapsed()
            self.running = False
        else:
            # Start
            self.elapsed_timer.start()
            self.running = True
        self.update()

    def reset_timer(self):
        self.running = False
        self.total_elapsed = 0
        self.update()

    def set_countdown(self, ms):
        self.countdown_target_ms = ms
        self.reset_timer()
        if hasattr(self.parent(), 'update_buttons'):
            self.parent().update_buttons()

    def get_elapsed_ms(self):
        ms = self.total_elapsed
        if self.running:
            ms += self.elapsed_timer.elapsed()
            
        if self.countdown_target_ms > 0:
            return self.countdown_target_ms - ms
        return ms

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stopwatch = StopWatch()
    stopwatch.resize(300, 300)
    stopwatch.show()
    sys.exit(app.exec())
