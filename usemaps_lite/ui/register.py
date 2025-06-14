import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog
from qgis.utils import iface
from qgis.PyQt.QtCore import Qt

from usemaps_lite.tools.translations import TRANSLATOR

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'register.ui'))


class RegisterDialog(QDialog, FORM_CLASS):
    """
    Dialog rejestracji usera i organizacji
    """

    def __init__(self):
        super(RegisterDialog, self).__init__(parent=iface.mainWindow())
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.cancel_button.clicked.connect(self.hide)

    def showEvent(self, event):
        super().showEvent(event)
        self.reg_email_line.clear()
        self.reg_orgname_line.clear()
        self.reg_pwd_line.clear()
        self.reg_pwd_again_line.clear()

        self.setWindowTitle(TRANSLATOR.translate_ui("register title"))
        self.email_label.setText(TRANSLATOR.translate_ui("email_label"))
        self.orgname_label.setText(TRANSLATOR.translate_ui("orgname_label"))
        self.password_label.setText(TRANSLATOR.translate_ui("password_label"))
        self.password_again_label.setText(TRANSLATOR.translate_ui("password_again_label"))
        self.register_button.setText(TRANSLATOR.translate_ui("register_button"))
        self.cancel_button.setText(TRANSLATOR.translate_ui("cancel"))
