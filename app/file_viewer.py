import subprocess
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel, QMessageBox
)


class FileViewerWindow(QWidget):
    def __init__(self, title: str, items: list):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(900, 520)
        self.items = items

        self.setup_ui(title)

    def setup_ui(self, title: str):
        layout = QVBoxLayout()

        label = QLabel(title)
        label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 8px;")

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Size", "Modified", "Score", "Path"])
        self.table.setRowCount(len(self.items))

        for row, item in enumerate(self.items):
            self.table.setItem(row, 0, QTableWidgetItem(item.get("name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(item.get("type", "")))
            self.table.setItem(row, 2, QTableWidgetItem(item.get("size", "")))
            self.table.setItem(row, 3, QTableWidgetItem(item.get("modified", "")))
            self.table.setItem(row, 4, QTableWidgetItem(item.get("score", "")))
            self.table.setItem(row, 5, QTableWidgetItem(item.get("path", "")))

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.cellDoubleClicked.connect(self.open_selected_item)

        layout.addWidget(label)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def open_selected_item(self, row, column):
        path_item = self.table.item(row, 5)

        if not path_item:
            return

        path = Path(path_item.text())

        if not path.exists():
            QMessageBox.warning(self, "Not Found", f"Path not found:\n{path}")
            return

        try:
            subprocess.Popen(f'explorer "{path}"', shell=True)
        except Exception as e:
            QMessageBox.critical(self, "Open Failed", f"Failed to open:\n{e}")