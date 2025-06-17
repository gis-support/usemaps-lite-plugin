from PyQt5.QtGui import QIcon

from usemaps_lite.ui.dockwidget import Dockwidget
from .resources import resources


class UsemapsLite:
    def __init__(self, iface):
        self.iface = iface
        self.dockwidget = None
        self.action = None

    def initGui(self):
        
        self.dockwidget = Dockwidget()

        self.action = self.dockwidget.toggleViewAction()
        icon = QIcon(":/plugins/usemapslite/zielen_v1.png")
        self.action.setIcon(icon)
        self.action.setText("GIS.Box Lite")

        self.toolbar = self.iface.addToolBar("GIS.Box Lite")
        self.toolbar.setObjectName("GIS.Box Lite")

        self.toolbar.addAction(self.action)
        
        self.dockwidget.layers.connect_layersremoved_signal(True)

    def unload(self):
        self.iface.removePluginMenu
        self.toolbar.clear()
        self.toolbar.deleteLater()
        self.dockwidget.layers.connect_layersremoved_signal(False)
        self.dockwidget.close()
