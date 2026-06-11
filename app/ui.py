import html
import traceback
from app.ui_logo import OrvixLogo
from app.command_parser import parse_command
from app.executor import execute_action
from app.file_viewer import FileViewerWindow
from app.intent_planner import plan_intent

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox,
    QMenu,
    QApplication,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer
from PyQt6.QtGui import QMouseEvent, QTextCursor


class OrvixWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.viewer_windows = []
        self.expanded = False
        self.drag_position = None
        self.is_dragging = False

        self.orb_size = 62
        self.panel_width = 520
        self.panel_height = 650

        self.setWindowTitle("Orvix")
        self.setGeometry(860, 220, self.orb_size, self.orb_size)

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setup_ui()
        self.set_status("ready")
        self.add_log("Orvix ready.", "success")
        self.add_log("Type a command below or use a quick action.", "info")

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget#mainContainer {
                background-color: rgba(8, 12, 24, 238);
                border-radius: 30px;
                border: 1px solid rgba(255, 255, 255, 38);
            }

            QLabel#orb {
                background-color: qradialgradient(
                    cx:0.35, cy:0.28, radius:0.85,
                    fx:0.35, fy:0.28,
                    stop:0 #f8fafc,
                    stop:0.18 #c4b5fd,
                    stop:0.48 #6366f1,
                    stop:1 #020617
                );
                color: white;
                border-radius: 31px;
                font-size: 26px;
                font-weight: 900;
                border: 2px solid rgba(255,255,255,105);
            }

            QLabel#miniOrb {
                background-color: qradialgradient(
                    cx:0.35, cy:0.28, radius:0.85,
                    fx:0.35, fy:0.28,
                    stop:0 #f8fafc,
                    stop:0.18 #c4b5fd,
                    stop:0.48 #6366f1,
                    stop:1 #020617
                );
                color: white;
                border-radius: 22px;
                font-size: 21px;
                font-weight: 900;
                border: 2px solid rgba(255,255,255,90);
            }

            QLabel#title {
                font-size: 24px;
                font-weight: 900;
                color: #f8fafc;
                letter-spacing: -0.5px;
            }

            QLabel#subtitle {
                font-size: 12px;
                color: #94a3b8;
                font-weight: 600;
            }

            QLabel#statusDot {
                background-color: #22c55e;
                border-radius: 6px;
                min-width: 12px;
                max-width: 12px;
                min-height: 12px;
                max-height: 12px;
            }

            QLabel#statusText {
                color: #cbd5e1;
                font-size: 12px;
                font-weight: 700;
            }

            QLabel#sectionLabel {
                color: #94a3b8;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1.4px;
                text-transform: uppercase;
            }

            QTextEdit {
                background-color: rgba(255, 255, 255, 18);
                border: 1px solid rgba(255, 255, 255, 34);
                border-radius: 20px;
                padding: 12px;
                color: #e5e7eb;
                font-size: 13px;
                font-family: Segoe UI;
                selection-background-color: #6366f1;
            }

            QLineEdit {
                background-color: rgba(255, 255, 255, 24);
                border: 1px solid rgba(255, 255, 255, 48);
                border-radius: 18px;
                padding: 14px 16px;
                color: #f8fafc;
                font-size: 14px;
                font-family: Segoe UI;
            }

            QLineEdit:focus {
                border: 1px solid rgba(129, 140, 248, 170);
                background-color: rgba(255, 255, 255, 30);
            }

            QPushButton {
                background-color: #6366f1;
                border: none;
                border-radius: 16px;
                padding: 12px 16px;
                color: white;
                font-weight: 800;
                font-family: Segoe UI;
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #818cf8;
            }

            QPushButton:pressed {
                background-color: #4f46e5;
            }

            QPushButton:disabled {
                background-color: rgba(148, 163, 184, 60);
                color: rgba(255, 255, 255, 120);
            }

            QPushButton#ghostButton {
                background-color: rgba(255,255,255,22);
                color: #e5e7eb;
            }

            QPushButton#ghostButton:hover {
                background-color: rgba(255,255,255,44);
            }

            QPushButton#quickButton {
                background-color: rgba(255,255,255,16);
                border: 1px solid rgba(255,255,255,28);
                color: #cbd5e1;
                border-radius: 999px;
                padding: 8px 12px;
                font-size: 11px;
                font-weight: 700;
            }

            QPushButton#quickButton:hover {
                background-color: rgba(99,102,241,70);
                color: white;
            }

            QPushButton#runButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1,
                    stop:1 #8b5cf6
                );
                min-height: 44px;
            }

            QPushButton#clearButton {
                background-color: rgba(255,255,255,18);
                color: #cbd5e1;
            }

            QPushButton#clearButton:hover {
                background-color: rgba(239, 68, 68, 75);
                color: white;
            }
        """)

        self.main_container = QWidget(self)
        self.main_container.setObjectName("mainContainer")
        self.main_container.setGeometry(0, 0, self.orb_size, self.orb_size)

        self.layout = QVBoxLayout(self.main_container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.orb = OrvixLogo(self.orb_size, self.main_container)
        self.orb.setObjectName("orb")

        self.orb.mousePressEvent = self.orb_mouse_press
        self.orb.mouseMoveEvent = self.orb_mouse_move
        self.orb.mouseReleaseEvent = self.orb_mouse_release

        self.layout.addWidget(self.orb)

        self.panel = QWidget(self.main_container)
        self.panel.setVisible(False)

        panel_layout = QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(20, 16, 20, 20)
        panel_layout.setSpacing(14)

        header = QHBoxLayout()
        header.setSpacing(12)

        title_block = QVBoxLayout()
        title_block.setSpacing(1)

        title = QLabel("Orvix")
        title.setObjectName("title")

        subtitle = QLabel("Desktop AI Agent")
        subtitle.setObjectName("subtitle")

        title_block.addWidget(title)
        title_block.addWidget(subtitle)

        status_layout = QHBoxLayout()
        status_layout.setSpacing(8)

        self.status_dot = QLabel()
        self.status_dot.setObjectName("statusDot")
        self.status_dot.setFixedSize(12, 12)

        self.status_text = QLabel("Ready")
        self.status_text.setObjectName("statusText")

        status_layout.addWidget(self.status_dot)
        status_layout.addWidget(self.status_text)

        collapse_btn = QPushButton("–")
        collapse_btn.setObjectName("ghostButton")
        collapse_btn.setFixedWidth(42)
        collapse_btn.clicked.connect(self.collapse)

        close_btn = QPushButton("×")
        close_btn.setObjectName("ghostButton")
        close_btn.setFixedWidth(42)
        close_btn.clicked.connect(QApplication.quit)

        header.addLayout(title_block)
        header.addStretch()
        header.addLayout(status_layout)
        header.addWidget(collapse_btn)
        header.addWidget(close_btn)

        quick_label = QLabel("Quick actions")
        quick_label.setObjectName("sectionLabel")

        quick_row_1 = QHBoxLayout()
        quick_row_1.setSpacing(8)

        quick_commands_1 = [
            ("Word", "create a word file named TestAI about Science and AI"),
            ("PPT", "create ppt named TestPPT about Artificial Intelligence in 6 slides"),
        ]

        for label, command in quick_commands_1:
            button = QPushButton(label)
            button.setObjectName("quickButton")
            button.clicked.connect(lambda checked=False, cmd=command: self.fill_command(cmd))
            quick_row_1.addWidget(button)

        quick_row_2 = QHBoxLayout()
        quick_row_2.setSpacing(8)

        quick_commands_2 = [
            ("React", "create premium react portfolio named TestPortfolio on desktop open in vs code and run it"),
            ("Summarize", "summarize this document"),
        ]

        for label, command in quick_commands_2:
            button = QPushButton(label)
            button.setObjectName("quickButton")
            button.clicked.connect(lambda checked=False, cmd=command: self.fill_command(cmd))
            quick_row_2.addWidget(button)

        activity_label = QLabel("Activity")
        activity_label.setObjectName("sectionLabel")

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        input_label = QLabel("Command")
        input_label.setObjectName("sectionLabel")

        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Ask Orvix: create a Word file, generate PPT, open VS Code...")
        self.command_input.returnPressed.connect(self.handle_command)

        self.run_btn = QPushButton("Run")
        self.run_btn.setObjectName("runButton")
        self.run_btn.setFixedWidth(88)
        self.run_btn.clicked.connect(self.handle_command)

        input_row.addWidget(self.command_input)
        input_row.addWidget(self.run_btn)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(10)

        self.clear_btn = QPushButton("Clear activity")
        self.clear_btn.setObjectName("clearButton")
        self.clear_btn.clicked.connect(self.clear_log)

        bottom_row.addWidget(self.clear_btn)
        bottom_row.addStretch()

        panel_layout.addLayout(header)
        panel_layout.addWidget(quick_label)
        panel_layout.addLayout(quick_row_1)
        panel_layout.addLayout(quick_row_2)
        panel_layout.addWidget(activity_label)
        panel_layout.addWidget(self.log_box)
        panel_layout.addWidget(input_label)
        panel_layout.addLayout(input_row)
        panel_layout.addLayout(bottom_row)

        self.orb.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.orb.customContextMenuRequested.connect(self.show_context_menu)

    def fill_command(self, command: str):
        self.command_input.setText(command)
        self.command_input.setFocus()

    def clear_log(self):
        self.log_box.clear()
        self.set_status("ready")
        self.add_log("Orvix ready.", "success")
        self.add_log("Activity cleared. Type a new command below.", "info")

    def add_log(self, message: str, level: str = "info"):
        safe_message = html.escape(str(message)).replace("\n", "<br>")

        colors = {
            "info": "#cbd5e1",
            "success": "#86efac",
            "working": "#fde68a",
            "error": "#fca5a5",
            "command": "#bfdbfe",
            "plan": "#ddd6fe",
        }

        border_colors = {
            "info": "rgba(148, 163, 184, 0.28)",
            "success": "rgba(34, 197, 94, 0.45)",
            "working": "rgba(250, 204, 21, 0.45)",
            "error": "rgba(239, 68, 68, 0.45)",
            "command": "rgba(96, 165, 250, 0.48)",
            "plan": "rgba(167, 139, 250, 0.48)",
        }

        labels = {
            "info": "INFO",
            "success": "DONE",
            "working": "WORKING",
            "error": "ERROR",
            "command": "COMMAND",
            "plan": "PLAN",
        }

        color = colors.get(level, colors["info"])
        border = border_colors.get(level, border_colors["info"])
        label = labels.get(level, "INFO")

        html_block = f"""
        <div style="
            margin: 8px 0;
            padding: 10px 12px;
            border-radius: 12px;
            border: 1px solid {border};
            background: rgba(255,255,255,0.045);
        ">
            <div style="
                color: {color};
                font-size: 10px;
                font-weight: 800;
                letter-spacing: 1.2px;
                margin-bottom: 4px;
            ">{label}</div>
            <div style="
                color: #e5e7eb;
                font-size: 13px;
                line-height: 1.45;
            ">{safe_message}</div>
        </div>
        """

        self.log_box.append(html_block)
        self.log_box.moveCursor(QTextCursor.MoveOperation.End)

    def set_status(self, status: str, text: str = None):
        colors = {
            "ready": "#22c55e",
            "working": "#facc15",
            "error": "#ef4444",
        }

        labels = {
            "ready": "Ready",
            "working": "Working",
            "error": "Needs attention",
        }

        color = colors.get(status, "#22c55e")
        label = text or labels.get(status, "Ready")

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

        self.status_text.setText(label)

    def set_busy(self, busy: bool):
        self.run_btn.setDisabled(busy)
        self.command_input.setDisabled(busy)
        self.clear_btn.setDisabled(busy)

        if busy:
            self.set_status("working", "Executing")
        else:
            self.set_status("ready", "Ready")

        QApplication.processEvents()

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
        clear_action = menu.addAction("Clear Activity")
        exit_action = menu.addAction("Exit")

        action = menu.exec(self.mapToGlobal(position))

        if action == toggle_action:
            if self.expanded:
                self.collapse()
            else:
                self.expand()

        elif action == clear_action:
            self.clear_log()

        elif action == exit_action:
            QApplication.quit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self.expanded:
                self.collapse()
            event.accept()
            return

        QWidget.keyPressEvent(self, event)

    def orb_mouse_press(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.position().toPoint())
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
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(10)

        top_layout = QHBoxLayout()
        self.orb.setObjectName("miniOrb")
        self.orb.set_logo_size(44)

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

            if item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().setParent(None)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.orb.setParent(self.main_container)
        self.orb.setObjectName("orb")
        self.orb.set_logo_size(self.orb_size)
        self.orb.setStyleSheet("")

        self.layout.addWidget(self.orb)
        self.main_container.setGeometry(0, 0, self.orb_size, self.orb_size)

    def resizeEvent(self, event):
        self.main_container.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.position().toPoint())
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
        command = self.command_input.text().strip()

        if not command:
            self.add_log("Please type a command first.", "error")
            return

        self.set_busy(True)
        self.add_log(command, "command")
        self.add_log("Understanding command...", "working")

        QTimer.singleShot(40, lambda: self.execute_command(command))

    def execute_command(self, command: str):
        try:
            planned_result = plan_intent(command)

            if isinstance(planned_result, dict) and planned_result.get("action") == "display_message":
                self.add_log(planned_result.get("message", "Done."), "info")
                self.command_input.clear()
                self.set_busy(False)
                return

            if isinstance(planned_result, dict):
                parsed = planned_result
                self.add_log("Validated action plan created.", "plan")
            else:
                if planned_result != command:
                    self.add_log(f"Planned command: {planned_result}", "plan")

                parsed = parse_command(planned_result)

            if not parsed.get("success"):
                self.add_log(parsed.get("message", "Could not understand command."), "error")
                self.command_input.clear()
                self.set_status("error")
                self.set_busy(False)
                return

            if self.has_risky_action(parsed):
                confirm = self.show_delete_confirmation(parsed)

                if not confirm:
                    self.add_log("Delete cancelled by user.", "info")
                    self.command_input.clear()
                    self.set_busy(False)
                    return

                self.add_log("Delete confirmed by user.", "working")

            self.add_log(f"Action detected: {parsed.get('action')}", "plan")
            self.add_log("Executing task...", "working")

            success, message = execute_action(parsed)
            self.display_result(success, message)

            self.command_input.clear()

            if success:
                self.set_status("ready", "Completed")
            else:
                self.set_status("error", "Failed")

            self.set_busy(False)

        except Exception as error:
            self.add_log(f"Crash: {error}", "error")
            self.add_log(traceback.format_exc(), "error")
            self.set_status("error", "Crashed")
            self.set_busy(False)

    def display_result(self, success, message):
        level = "success" if success else "error"
        prefix = "Completed" if success else "Failed"

        if isinstance(message, dict):
            text = message.get("text", "")

            if text:
                self.add_log(f"{prefix}: {text}", level)
            else:
                self.add_log(prefix, level)

            viewer_data = message.get("viewer")

            if viewer_data:
                viewer = FileViewerWindow(
                    viewer_data.get("title", "File Viewer"),
                    viewer_data.get("items", [])
                )
                viewer.show()
                self.viewer_windows.append(viewer)

            return

        self.add_log(f"{prefix}: {message}", level)

    def has_risky_action(self, parsed_command):
        if parsed_command.get("action") == "delete":
            return True

        if parsed_command.get("action") == "multi_step":
            for step in parsed_command.get("steps", []):
                if step.get("action") == "delete":
                    return True

        return False

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

    def closeEvent(self, event):
        QApplication.quit()
        event.accept()