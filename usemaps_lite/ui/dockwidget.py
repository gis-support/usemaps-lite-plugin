import os

from PyQt5 import uic, QtWidgets
from qgis.utils import iface
from qgis.PyQt.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel

from usemaps_lite.tools.event_handler import EVENT_HANDLER
from usemaps_lite.tools.user_mapper import USER_MAPPER
from usemaps_lite.tools.auth import Auth
from usemaps_lite.tools.organization import Organization
from usemaps_lite.tools.layers import Layers

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dockwidget.ui'))

class Dockwidget(QtWidgets.QDockWidget, FORM_CLASS):
    """
    Główna klasa widgetu wtyczki.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        iface.addDockWidget(Qt.RightDockWidgetArea, self)

        self.layers_model = QStandardItemModel()
        self.layers_listview.setModel(self.layers_model)

        self.users_tableview_model = QStandardItemModel()
        self.users_tableview_model.setHorizontalHeaderLabels(['Email', 'Zweryfikowany'])
        self.users_tableview.setModel(self.users_tableview_model)    
        
        USER_MAPPER.set_users_model(self.users_tableview_model)
    
        self.events_listview_model = QStandardItemModel()
        self.events_listview.setModel(self.events_listview_model)

        EVENT_HANDLER.set_events_listview_model(self.events_listview_model)

        self.auth = Auth(self)
        self.organization = Organization(self)
        self.layers = Layers(self)
        
        self.layers_tab.setEnabled(False)
        self.users_tab.setEnabled(False)
        self.logout_button.setVisible(False)
