from PySide6.QtWidgets import QApplication
from widget import MainWidget

app = QApplication()
window = MainWidget()
window.show()
app.exec()