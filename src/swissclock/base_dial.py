# SPDX-License-Identifier: GPL-3.0-or-later
from PySide6.QtCore import QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QMenu, QMessageBox, QWidget


class BaseDial(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dial)
        self.timer.start(30) # Smooth animation
        
        self.black_color = QColor(0, 0, 0)
        self.red_color = QColor(220, 0, 0) # Swiss red
        self.green_color = QColor(0, 180, 0) # Normal tracking green
        self.orange_color = QColor(255, 165, 0) # Warning orange

    def update_dial(self):
        self.update()

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 240.0, side / 240.0)

        # White background face
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        painter.drawEllipse(-98, -98, 196, 196)
        
        self.draw_face(painter)
        self.draw_hands(painter)

    def draw_face(self, painter):
        pass

    def draw_hands(self, painter):
        pass

    def draw_dial(self, painter):
        # To be implemented by subclasses
        pass

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        about_action = menu.addAction("About")
        help_action = menu.addAction("Help (Shortcuts)")
        action = menu.exec(event.globalPos())
        if action == about_action:
            self.show_about()
        elif action == help_action:
            self.show_help()

    def show_help(self):
        QMessageBox.information(self, "SwissClock Help",
            "<h2>Keyboard Shortcuts</h2>"
            "<ul>"
            "<li><b>T</b>: Switch between Clock and Stopwatch</li>"
            "<li><b>Space</b>: Start / Stop / Resume Stopwatch</li>"
            "<li><b>R</b>: Reset Stopwatch</li>"
            "<li><b>D</b>: Toggle Digital / Analog mode (in Stopwatch)</li>"
            "<li><b>F</b>: Toggle Fullscreen mode</li>"
            "</ul>")

    def show_about(self):
        QMessageBox.about(self, "About SwissClock",
            "<h2>Swiss Railway Time</h2>"
            "<p>A Swiss Railways inspired unified analog clock and morphing digital stopwatch.</p>"
            "<p><b>Author:</b> Alin Elena &lt;alin@elena.re&gt;</p>"
            "<p><b>License:</b> GPL-3.0-or-later</p>"
            "<p><b>Dependencies:</b> PySide6</p>")

    def draw_capsule_hand(self, painter, angle, color, rect_args):
        painter.save()
        painter.rotate(angle)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        # rect_args: (x, y, w, h, xRadius, yRadius)
        painter.drawRoundedRect(*rect_args)
        painter.restore()

    def draw_swiss_second_hand(self, painter, angle):
        painter.save()
        painter.rotate(angle)
        painter.setBrush(self.red_color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(-1, -76, 2, 101)
        painter.drawEllipse(QRectF(-6, -82, 12, 12))
        painter.drawEllipse(QRectF(-3, -3, 6, 6))
        painter.restore()
