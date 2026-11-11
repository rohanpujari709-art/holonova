import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class HoloFanStudio(QMainWindow):

    def __init__(self):
        super().__init__()

        # Window Title
        self.setWindowTitle("HoloFan Studio")

        # Window Size
        self.setGeometry(200, 100, 1000, 700)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Vertical Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Open Image Button
        self.open_image_button = QPushButton("Open Image")
        self.layout.addWidget(self.open_image_button)
        self.open_image_button.clicked.connect(self.open_image)

        # Preview Label
        self.image_label = QLabel("No Image Selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)


# Create the application
app = QApplication(sys.argv)

# Create the main window
window = HoloFanStudio()
window.show()

# Run the application
sys.exit(app.exec())
