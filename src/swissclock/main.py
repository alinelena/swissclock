# SPDX-License-Identifier: GPL-3.0-or-later
import sys

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .clock import AnalogClock
from .stop import StopWatch


class UnifiedApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Swiss Railway Time")
        self.resize(320, 420)
        
        layout = QVBoxLayout(self)
        
        self.stacked = QStackedWidget()
        
        self.clock_widget = AnalogClock()
        self.stopwatch_widget = StopWatch(self)
        
        self.stacked.addWidget(self.clock_widget)
        self.stacked.addWidget(self.stopwatch_widget)
        
        layout.addWidget(self.stacked, 1) # Expanding
        
        # Action Buttons Layout (Start / Reset)
        self.action_layout = QHBoxLayout()
        self.btn_start = QPushButton("Start (Space)")
        self.btn_start.clicked.connect(self.toggle_stopwatch)
        
        self.btn_reset = QPushButton("Reset (R)")
        self.btn_reset.clicked.connect(self.reset_stopwatch)
        
        self.action_layout.addWidget(self.btn_start)
        self.action_layout.addWidget(self.btn_reset)
        
        # Only show action buttons when in stopwatch mode
        self.action_widget = QWidget()
        self.action_widget.setLayout(self.action_layout)
        sp = self.action_widget.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.action_widget.setSizePolicy(sp)
        self.action_widget.setVisible(False)
        layout.addWidget(self.action_widget)
        
        # Main Toggle Button
        self.btn_toggle = QPushButton("Switch to Stopwatch (T)")
        self.btn_toggle.clicked.connect(self.toggle_view)
        layout.addWidget(self.btn_toggle)

        # Bulletproof window-level shortcuts
        self.shortcut_toggle = QShortcut(QKeySequence("T"), self)
        self.shortcut_toggle.activated.connect(self.toggle_view)
        
        self.shortcut_space = QShortcut(QKeySequence("Space"), self)
        self.shortcut_space.activated.connect(self.handle_space)
        
        self.shortcut_reset = QShortcut(QKeySequence("R"), self)
        self.shortcut_reset.activated.connect(self.handle_reset)
        
        self.shortcut_digital = QShortcut(QKeySequence("D"), self)
        self.shortcut_digital.activated.connect(self.handle_digital)
        
        self.shortcut_fullscreen = QShortcut(QKeySequence("F"), self)
        self.shortcut_fullscreen.activated.connect(self.toggle_fullscreen)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def handle_space(self):
        if self.stacked.currentIndex() == 1:
            self.toggle_stopwatch()

    def handle_reset(self):
        if self.stacked.currentIndex() == 1:
            self.reset_stopwatch()
            
    def handle_digital(self):
        if self.stacked.currentIndex() == 1:
            self.stopwatch_widget.toggle_digital_mode()

    def toggle_stopwatch(self):
        self.stopwatch_widget.toggle_timer()
        self.update_buttons()
        
    def reset_stopwatch(self):
        self.stopwatch_widget.reset_timer()
        self.update_buttons()

    def update_buttons(self):
        if self.stopwatch_widget.running:
            self.btn_start.setText("Stop (Space)")
        else:
            if self.stopwatch_widget.total_elapsed > 0:
                self.btn_start.setText("Resume (Space)")
            else:
                self.btn_start.setText("Start (Space)")
        
    def toggle_view(self):
        if self.stacked.currentIndex() == 0:
            self.stacked.setCurrentIndex(1)
            self.btn_toggle.setText("Switch to Clock (T)")
            self.action_widget.setVisible(True)
            self.update_buttons()
        else:
            self.stacked.setCurrentIndex(0)
            self.btn_toggle.setText("Switch to Stopwatch (T)")
            self.action_widget.setVisible(False)

def main():
    app = QApplication(sys.argv)
    
    # Optional: Set an application-wide stylesheet for a modern dark look if desired
    app.setStyleSheet("""
        QWidget {
            background-color: #121212;
        }
    """)
    
    clock = UnifiedApp()
    clock.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
