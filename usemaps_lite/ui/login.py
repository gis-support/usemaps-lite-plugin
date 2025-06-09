import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog
from qgis.utils import iface
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsSettings

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'login.ui'))


class LoginDialog(QDialog, FORM_CLASS):
    """
    Dialog logowania do Usemaps Lite.
    """

    def __init__(self):
        super(LoginDialog, self).__init__(parent=iface.mainWindow())
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.cancel_button.clicked.connect(self.hide)

    def showEvent(self, event):
        super().showEvent(event)
        settings = QgsSettings()

        username = settings.value("usemaps_lite/login", "", type=str)
        pwd = settings.value("usemaps_lite/pwd", "", type=str)
        
        if username and pwd:
            self.log_email_line.setText(username)
            self.log_pwd_line.setText(pwd)
        else:
            self.log_email_line.clear()
            self.log_pwd_line.clear()
