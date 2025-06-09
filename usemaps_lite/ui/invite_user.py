import os
import re

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog
from qgis.utils import iface
from qgis.PyQt.QtCore import Qt

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'invite_user.ui'))


class InviteUserDialog(QDialog, FORM_CLASS):
    """
    Dialog zapraszania ludzi do organizacji.
    """

    def __init__(self):
        super(InviteUserDialog, self).__init__(parent=iface.mainWindow())
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.cancel_button.clicked.connect(self.hide)
        self.email_line.textChanged.connect(self.verify_email)

    def showEvent(self, event):
        super().showEvent(event)
        self.email_line.clear()
        self.invite_user_button.setEnabled(False)

    def verify_email(self, email: str):
        """
        Prosty walidator maili.
        """

        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        self.invite_user_button.setEnabled(False)
        if re.match(pattern, email) is not None:
            self.invite_user_button.setEnabled(True)
