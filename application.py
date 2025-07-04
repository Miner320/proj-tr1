from PySide6.QtWidgets import QApplication
from widget import MainWidget
import sys

app = QApplication()
window = MainWidget(server_addr='localhost', server_port=sys.argv[1] if len(sys.argv) > 1 else 64000,client_addr='localhost', client_port=sys.argv[2] if len(sys.argv) > 2 else '64001')
window.show()
app.exec()