import traceback
from app.command_parser import parse_command
from app.executor import execute_action
from app.file_viewer import FileViewerWindow
from app.intent_planner import plan_intent
from PyQt6.QtWidgets import (
  QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
QLineEdit, QPushButton, QLabel, QMessageBox, QMenu, QApplication
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import QMouseEvent


class OrvixWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.viewer_windows = []
        self.expanded = False
        self.drag_position = None
        self.is_dragging = False

        self.orb_size = 58
        self.panel_width = 430
        self.panel_height = 520

        self.setWindowTitle("Orvix")
        self.setGeometry(900, 250, self.orb_size, self.orb_size)

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setup_ui()
        self.set_status("ready")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self.expanded:
                self.collapse()
            event.accept()
            return

        QWidget.keyPressEvent(self, event)
    
    def set_status(self, status: str):
        colors = {
            "ready": "#22c55e",
            "working": "#facc15",
            "error": "#ef4444"
        }

        color = colors.get(status, "#22c55e")

        self.status_dot.setStyleSheet(f"""
            QLabel#statusDot {{
                background-color: {color};
                border-radius: 6px;
                min-width: 12px;
                max-width: 12px;
                min-height: 12px;
                max-height: 12px;
            }}
        """)
    def setup_ui(self):
        self.setStyleSheet("""
            QWidget#mainContainer {
                background-color: rgba(18, 22, 32, 235);
                border-radius: 28px;
                border: 1px solid rgba(255, 255, 255, 35);
            }
                        QLabel#statusDot {
                background-color: #22c55e;
                border-radius: 6px;
                min-width: 12px;
                max-width: 12px;
                min-height: 12px;
                max-height: 12px;
            }
            QLabel#orb {
                background-color: qradialgradient(
                    cx:0.35, cy:0.3, radius:0.8,
                    fx:0.35, fy:0.3,
                    stop:0 #a5b4fc,
                    stop:0.45 #6366f1,
                    stop:1 #111827
                );
                color: white;
                border-radius: 29px;
                font-size: 25px;
                font-weight: bold;
                border: 2px solid rgba(255,255,255,90);
            }

            QLabel#title {
                font-size: 22px;
                font-weight: bold;
                color: white;
            }

            QTextEdit {
                background-color: rgba(255, 255, 255, 24);
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 14px;
                padding: 10px;
                color: white;
                font-size: 13px;
                font-family: Segoe UI;
            }

            QLineEdit {
                background-color: rgba(255, 255, 255, 30);
                border: 1px solid rgba(255, 255, 255, 55);
                border-radius: 14px;
                padding: 11px;
                color: white;
                font-size: 14px;
                font-family: Segoe UI;
            }

            QPushButton {
                background-color: #6366f1;
                border: none;
                border-radius: 14px;
                padding: 10px;
                color: white;
                font-weight: bold;
                font-family: Segoe UI;
            }

            QPushButton:hover {
                background-color: #818cf8;
            }

            QPushButton#ghostButton {
                background-color: rgba(255,255,255,25);
            }

            QPushButton#ghostButton:hover {
                background-color: rgba(255,255,255,45);
            }
        """)

        self.main_container = QWidget(self)
        self.main_container.setObjectName("mainContainer")
        self.main_container.setGeometry(0, 0, self.orb_size, self.orb_size)

        self.layout = QVBoxLayout(self.main_container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.orb = QLabel("✦", self.main_container)
        self.orb.setObjectName("orb")
        self.orb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.orb.setFixedSize(self.orb_size, self.orb_size)

        self.orb.mousePressEvent = self.orb_mouse_press
        self.orb.mouseMoveEvent = self.orb_mouse_move
        self.orb.mouseReleaseEvent = self.orb_mouse_release

        self.layout.addWidget(self.orb)

        self.panel = QWidget(self.main_container)
        self.panel.setVisible(False)

        panel_layout = QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(18, 14, 18, 18)

        header = QHBoxLayout()
        title = QLabel("Orvix")
        title.setObjectName("title")
        self.status_dot = QLabel()
        self.status_dot.setObjectName("statusDot")
        self.status_dot.setFixedSize(12, 12)
        collapse_btn = QPushButton("–")
        collapse_btn.setObjectName("ghostButton")
        collapse_btn.setFixedWidth(42)
        collapse_btn.clicked.connect(self.collapse)

        close_btn = QPushButton("×")
        close_btn.setObjectName("ghostButton")
        close_btn.setFixedWidth(42)
        close_btn.clicked.connect(QApplication.quit)

        header.addWidget(title)
        header.addWidget(self.status_dot)
        header.addStretch()
        header.addWidget(collapse_btn)
        header.addWidget(close_btn)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.append("Orvix ready.")
        self.log_box.append("Type a command below.")

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Ask Orvix to do something...")
        self.command_input.returnPressed.connect(self.handle_command)

        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.handle_command)

        panel_layout.addLayout(header)
        panel_layout.addWidget(self.log_box)
        panel_layout.addWidget(self.command_input)
        panel_layout.addWidget(self.run_btn)
        self.orb.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.orb.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #111827;
                color: white;
                border: 1px solid rgba(255,255,255,60);
                border-radius: 8px;
                padding: 6px;
            }

            QMenu::item {
                padding: 8px 22px;
                border-radius: 6px;
            }

            QMenu::item:selected {
                background-color: #6366f1;
            }
        """)

        toggle_action = menu.addAction("Collapse" if self.expanded else "Expand")
        clear_action = menu.addAction("Clear Log")
        exit_action = menu.addAction("Exit")

        action = menu.exec(position)

        if action == toggle_action:
            if self.expanded:
                self.collapse()
            else:
                self.expand()

        elif action == clear_action:
            self.log_box.clear()
            self.log_box.append("Orvix ready.")
            self.log_box.append("Type a command below.")
            self.set_status("ready")

        elif action == exit_action:
             QApplication.quit()
            
    def orb_mouse_press(self, event):
      if event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.globalPosition().toPoint())
            event.accept()
            return

      if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.is_dragging = False
            event.accept()

    def orb_mouse_move(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.is_dragging = True
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def orb_mouse_release(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.is_dragging:
                if self.expanded:
                    self.collapse()
                else:
                    self.expand()

            self.drag_position = None
            self.is_dragging = False
            event.accept()

    def expand(self):
        if self.expanded:
            return

        self.expanded = True
        self.panel.setVisible(True)

        self.layout.removeWidget(self.orb)
        self.layout.setContentsMargins(10, 10, 10, 10)

        top_layout = QHBoxLayout()
        self.orb.setFixedSize(48, 48)
        self.orb.setStyleSheet("""
            QLabel#orb {
                background-color: #6366f1;
                color: white;
                border-radius: 24px;
                font-size: 22px;
                font-weight: bold;
                border: 2px solid rgba(255,255,255,90);
            }
        """)

        top_layout.addWidget(self.orb)
        top_layout.addStretch()

        self.layout.addLayout(top_layout)
        self.layout.addWidget(self.panel)

        start = self.geometry()
        end = QRect(start.x(), start.y(), self.panel_width, self.panel_height)

        self.animate_geometry(start, end)
        self.command_input.setFocus()

    def collapse(self):
        if not self.expanded:
            return

        self.expanded = False

        start = self.geometry()
        end = QRect(start.x(), start.y(), self.orb_size, self.orb_size)

        self.animate_geometry(start, end, collapse=True)

    def animate_geometry(self, start, end, collapse=False):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(260)
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        if collapse:
            self.animation.finished.connect(self.finish_collapse)

        self.animation.start()

    def finish_collapse(self):
        self.panel.setVisible(False)

        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.orb.setParent(self.main_container)
        self.orb.setFixedSize(self.orb_size, self.orb_size)
        self.orb.setStyleSheet("")

        self.layout.addWidget(self.orb)
        self.main_container.setGeometry(0, 0, self.orb_size, self.orb_size)

    def resizeEvent(self, event):
        self.main_container.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.globalPosition().toPoint())
            event.accept()
            return

        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.is_dragging = False
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.is_dragging = True
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.drag_position = None
        self.is_dragging = False
        event.accept()
    
    def handle_command(self):
        try:
            command = self.command_input.text().strip()

            if not command:
                self.log_box.append("Please type a command.")
                return

            self.set_status("working")
            self.log_box.append(f"> {command}")
            self.log_box.append("Understanding command...")

            planned_result = plan_intent(command)

            if isinstance(planned_result, dict):
                parsed = planned_result
                self.log_box.append("Planned: validated action plan")
            else:
                if planned_result != command:
                    self.log_box.append(f"Planned: {planned_result}")

                parsed = parse_command(planned_result)

            if not parsed["success"]:
                self.log_box.append(parsed["message"])
                self.command_input.clear()
                self.set_status("error")
                return

            if self.has_risky_action(parsed):
                confirm = self.show_delete_confirmation(parsed)

                if not confirm:
                    self.log_box.append("Delete cancelled by user.")
                    self.command_input.clear()
                    self.set_status("ready")
                    return

                self.log_box.append("Delete confirmed by user.")

            self.log_box.append(f"Action detected: {parsed['action']}")
            self.log_box.append("Executing task...")

            success, message = execute_action(parsed)
            self.display_result(success, message)

            self.set_status("ready" if success else "error")
            self.command_input.clear()

        except Exception as e:
            self.log_box.append(f"CRASH: {e}")
            self.log_box.append(traceback.format_exc())
            self.set_status("error")
    def display_result(self, success, message):
        prefix = "✓" if success else "✗"

        if isinstance(message, dict):
            text = message.get("text", "")
            self.log_box.append(f"{prefix} {text}")

            viewer_data = message.get("viewer")
            if viewer_data:
                viewer = FileViewerWindow(
                    viewer_data.get("title", "File Viewer"),
                    viewer_data.get("items", [])
                )
                viewer.show()
                self.viewer_windows.append(viewer)

            return

        self.log_box.append(f"{prefix} {message}")

    def has_risky_action(self, parsed_command):
        if parsed_command.get("action") == "delete":
            return True

        if parsed_command.get("action") == "multi_step":
            for step in parsed_command.get("steps", []):
                if step.get("action") == "delete":
                    return True

        return False

    def closeEvent(self, event):
        QApplication.quit()
        event.accept()    
    
    def show_delete_confirmation(self, parsed_command):
        delete_steps = []

        if parsed_command.get("action") == "delete":
            delete_steps.append(parsed_command)

        if parsed_command.get("action") == "multi_step":
            for step in parsed_command.get("steps", []):
                if step.get("action") == "delete":
                    delete_steps.append(step)

        names = []
        for step in delete_steps:
            item_type = step.get("item_type")
            name = step.get("name")
            location = step.get("location")
            names.append(f"{item_type}: {name} from {location}")

        message = "Do you want to delete this?\n\n" + "\n".join(names)

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        return reply == QMessageBox.StandardButton.Yes