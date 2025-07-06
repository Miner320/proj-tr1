from PySide6.QtWidgets import QApplication
from widget import MainWidget
import sys

app = QApplication()
window = MainWidget(server_addr="localhost", client_addr="localhost", client_port=64001, server_port=64000)
window.show()
app.exec()