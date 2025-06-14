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
from usemaps_lite.tools.translations import TRANSLATOR
from usemaps_lite.tools.delegate import CommentDelegate

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
        self.users_tableview_model.setHorizontalHeaderLabels([TRANSLATOR.translate_ui("email_label"),
                                                              TRANSLATOR.translate_ui("verified"),
                                                              TRANSLATOR.translate_ui("online")])
        self.users_tableview.setModel(self.users_tableview_model)    
        
        USER_MAPPER.set_users_model(self.users_tableview_model)
    
        self.events_listview_model = QStandardItemModel()
        self.events_listview.setModel(self.events_listview_model)
        self.events_listview.setItemDelegate(CommentDelegate())

        EVENT_HANDLER.set_events_listview_model(self.events_listview_model)

        self.auth = Auth(self)
        self.organization = Organization(self)
        self.layers = Layers(self)
        
        self.events_tab.setEnabled(False)
        self.layers_tab.setEnabled(False)
        self.users_tab.setEnabled(False)
        self.logout_button.setVisible(False)

        self.translate_interface()

    def translate_interface(self):
        
        # gorna czesc panelu, widoczna w kazdej zakladce
        
        self.info_label.setText(TRANSLATOR.translate_ui("info_label"))
        self.login_button.setText(TRANSLATOR.translate_ui("login_button"))
        self.register_button.setText(TRANSLATOR.translate_ui("register_button"))
        self.user_info_label.setText(TRANSLATOR.translate_ui("user"))
        self.logout_button.setText(TRANSLATOR.translate_ui("logout_button"))
        
        # zakładka Powiadomienia
        self.tabWidget.setTabText(0, TRANSLATOR.translate_ui("events_tab"))
        self.recent_activities_label.setText(TRANSLATOR.translate_ui("recent_activities_label"))
        self.comment_lineedit.setPlaceholderText(TRANSLATOR.translate_ui("comment_lineedit"))
        self.add_comment_button.setText(TRANSLATOR.translate_ui("add_comment_button"))
        
        # zakładka Dane
        self.tabWidget.setTabText(1, TRANSLATOR.translate_ui("layers_tab"))
        self.available_layers_label.setText(TRANSLATOR.translate_ui("available_layers_label"))
        self.layers_info_label.setText(TRANSLATOR.translate_ui("layers_info_label"))
        self.import_layer_button.setText(TRANSLATOR.translate_ui("import_layer_button"))
        self.remove_layer_button.setText(TRANSLATOR.translate_ui("remove_layer_button"))
        self.used_limit_label.setText(TRANSLATOR.translate_ui("used_limit_label"))
        
        # zakładka Organizacja
        self.tabWidget.setTabText(2, TRANSLATOR.translate_ui("users_tab"))
        self.org_members_label.setText(TRANSLATOR.translate_ui("coworkers"))
        self.org_info_label.setText(TRANSLATOR.translate_ui("org_info_label"))
        self.invite_user_button.setText(TRANSLATOR.translate_ui("invite_user_button"))
        self.remove_user_button.setText(TRANSLATOR.translate_ui("remove_user_button"))
