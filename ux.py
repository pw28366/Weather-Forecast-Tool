""" pyQT windows to show folium map"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    """To build Qt Window"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Trip weather forecast")
        self.resize(1024, 768)

        layout = QVBoxLayout()

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        view = QWebEngineView()
        layout.addWidget(view)

        view.setHtml(open("map.html").read())
