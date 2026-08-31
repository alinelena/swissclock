# SPDX-License-Identifier: GPL-3.0-or-later
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPen

# Define the 7 standard segments on a 1x2 grid
SEGS = [
    (0,0, 1,0), # 0: T
    (1,0, 1,1), # 1: TR
    (1,1, 1,2), # 2: BR
    (1,2, 0,2), # 3: B
    (0,2, 0,1), # 4: BL
    (0,1, 0,0), # 5: TL
    (0,1, 1,1)  # 6: M
]

# Standard 7-segment bitmasks for digits 0-9
# Order: T, TR, BR, B, BL, TL, M
STATES = [
    [1, 1, 1, 1, 1, 1, 0], # 0
    [0, 1, 1, 0, 0, 0, 0], # 1
    [1, 1, 0, 1, 1, 0, 1], # 2
    [1, 1, 1, 1, 0, 0, 1], # 3
    [0, 1, 1, 0, 0, 1, 1], # 4
    [1, 0, 1, 1, 0, 1, 1], # 5
    [1, 0, 1, 1, 1, 1, 1], # 6
    [1, 1, 1, 0, 0, 0, 0], # 7
    [1, 1, 1, 1, 1, 1, 1], # 8
    [1, 1, 1, 1, 0, 1, 1], # 9
]

class MorphDigit:
    def __init__(self):
        self.target = 0
        self.opacities = [float(x) for x in STATES[0]]
        
    def set_target(self, digit):
        if self.target != digit:
            self.target = digit
            
    def update(self):
        # Lerp each segment's opacity towards its target state (smooth fade)
        target_state = STATES[self.target]
        for i in range(7):
            current = self.opacities[i]
            target = float(target_state[i])
            
            # Smooth 30fps fade factor (lower is slower)
            factor = 0.1
            self.opacities[i] = current + (target - current) * factor
            
    def draw(self, painter, x_offset, y_offset, scale_x, scale_y, color):
        pen_width = max(2.0, scale_x * 0.15)
        
        # 10% gap to ensure the segments are completely distinct from each other
        gap = 0.1
        
        for i in range(7):
            opacity = self.opacities[i]
            if opacity < 0.01:
                continue
                
            x1, y1, x2, y2 = SEGS[i]
            
            dx = x2 - x1
            dy = y2 - y1
            length = (dx**2 + dy**2)**0.5
            
            # Apply gap to shrink the line slightly and make it distinct
            nx = dx / length
            ny = dy / length
            
            start_x = x1 + nx * gap
            start_y = y1 + ny * gap
            end_x = x2 - nx * gap
            end_y = y2 - ny * gap
            
            # Create a color with the current opacity for fading
            c = QColor(color)
            c.setAlphaF(opacity)
            
            pen = QPen(c)
            pen.setWidthF(pen_width)
            pen.setCapStyle(Qt.FlatCap) # Flat caps for that distinct LCD look
            painter.setPen(pen)
            
            painter.drawLine(QPointF(x_offset + start_x * scale_x, y_offset + start_y * scale_y),
                             QPointF(x_offset + end_x * scale_x, y_offset + end_y * scale_y))
