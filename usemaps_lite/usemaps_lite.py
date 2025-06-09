from PyQt5.QtGui import QIcon

from usemaps_lite.ui.dockwidget import Dockwidget


class UsemapsLite:
    def __init__(self, iface):
        self.iface = iface
        self.dockwidget = None
        self.action = None

    def initGui(self):
        
        self.dockwidget = Dockwidget()

        self.action = self.dockwidget.toggleViewAction()
        icon = QIcon(":/plugins/usemapslite/gissupport_logo.jpg")
        self.action.setIcon(icon)
        self.action.setText("Usemaps Lite")

        self.toolbar = self.iface.addToolBar("Usemaps Lite")
        self.toolbar.setObjectName("Usemaps Lite")

        self.toolbar.addAction(self.action)

    def unload(self):
        self.iface.removePluginMenu
        self.toolbar.clear()
        self.toolbar.deleteLater()
        self.dockwidget.close()
