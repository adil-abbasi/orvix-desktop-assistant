import sys
from PyQt6.QtWidgets import QApplication
from app.ui import OrvixWindow


def main():
    app = QApplication(sys.argv)
    window = OrvixWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()