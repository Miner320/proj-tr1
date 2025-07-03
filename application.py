from PySide6.QtWidgets import QApplication
from widget import InterfaceTransmissao

app = QApplication()
window = InterfaceTransmissao()
window.show()
app.exec()