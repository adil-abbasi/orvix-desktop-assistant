from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QBrush,
    QRadialGradient,
    QFont
)
from PyQt6.QtCore import Qt, QRectF, QPointF


class OrvixLogo(QWidget):
    def __init__(self, size=62, parent=None):
        super().__init__(parent)
        self.logo_size = size
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_logo_size(self, size):
        self.logo_size = size
        self.setFixedSize(size, size)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        w = self.width()
        h = self.height()
        s = min(w, h)

        outer_rect = QRectF(2, 2, s - 4, s - 4)
        inner_rect = QRectF(6, 6, s - 12, s - 12)

        # Outer glow
        glow = QRadialGradient(QPointF(s / 2, s / 2), s / 2)
        glow.setColorAt(0.0, QColor(129, 140, 248, 180))
        glow.setColorAt(0.45, QColor(99, 102, 241, 120))
        glow.setColorAt(1.0, QColor(2, 6, 23, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(outer_rect)

        # Main orb
        core_grad = QRadialGradient(QPointF(s * 0.38, s * 0.35), s * 0.58)
        core_grad.setColorAt(0.0, QColor(30, 41, 59))
        core_grad.setColorAt(0.35, QColor(15, 23, 42))
        core_grad.setColorAt(0.75, QColor(5, 10, 24))
        core_grad.setColorAt(1.0, QColor(2, 6, 23))
        painter.setBrush(QBrush(core_grad))
        painter.setPen(QPen(QColor(255, 255, 255, 70), 1.5))
        painter.drawEllipse(inner_rect)

        # Orbit ring 1
        orbit_pen = QPen(QColor(129, 140, 248, 170), max(1, s // 26))
        painter.setPen(orbit_pen)
        orbit1 = QRectF(s * 0.18, s * 0.18, s * 0.64, s * 0.64)
        painter.drawEllipse(orbit1)

        # Orbit ring 2
        orbit_pen_2 = QPen(QColor(56, 189, 248, 110), max(1, s // 34))
        painter.setPen(orbit_pen_2)
        orbit2 = QRectF(s * 0.27, s * 0.27, s * 0.46, s * 0.46)
        painter.drawEllipse(orbit2)

        # Center AI core
        center_grad = QRadialGradient(QPointF(s / 2, s / 2), s * 0.16)
        center_grad.setColorAt(0.0, QColor(255, 255, 255))
        center_grad.setColorAt(0.4, QColor(196, 181, 253))
        center_grad.setColorAt(1.0, QColor(99, 102, 241))
        painter.setBrush(QBrush(center_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        core_size = s * 0.18
        painter.drawEllipse(
            QRectF(
                (s - core_size) / 2,
                (s - core_size) / 2,
                core_size,
                core_size
            )
        )

        # Orbit nodes
        node_positions = [
            QPointF(s * 0.50, s * 0.18),
            QPointF(s * 0.77, s * 0.53),
            QPointF(s * 0.26, s * 0.72),
        ]

        node_colors = [
            QColor(125, 211, 252),
            QColor(52, 211, 153),
            QColor(196, 181, 253),
        ]

        node_radius = s * 0.06

        for pos, color in zip(node_positions, node_colors):
            node_grad = QRadialGradient(pos, node_radius)
            node_grad.setColorAt(0.0, QColor(255, 255, 255))
            node_grad.setColorAt(0.5, color)
            node_grad.setColorAt(1.0, QColor(color.red(), color.green(), color.blue(), 180))
            painter.setBrush(QBrush(node_grad))
            painter.setPen(QPen(QColor(255, 255, 255, 120), 1))
            painter.drawEllipse(
                QRectF(
                    pos.x() - node_radius / 2,
                    pos.y() - node_radius / 2,
                    node_radius,
                    node_radius
                )
            )

        # Optional tiny "O" identity in center
        font = QFont("Segoe UI", max(7, int(s * 0.18)))
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255, 210))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "O")