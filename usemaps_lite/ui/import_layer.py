import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QFrame
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.utils import iface


class DropFrame(QFrame):
    """
    Customowa klasa ramki ogarniająca przeciąganie i upuszczanie plików gpkg
    """

    file_dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith('.gpkg'):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith('.gpkg'):
                self.file_dropped.emit(file_path)
                return
        iface.messageBar().pushCritical("Usemaps Lite", f"Zły format pliku. Proszę wybrać plik w formacie .gpkg (GeoPackage).")

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'import_layer.ui'))


class ImportLayerDialog(QDialog, FORM_CLASS):
    """
    Dialog wgrywania warstw GPKG do organizacji
    """

    def __init__(self):
        super(ImportLayerDialog, self).__init__(parent=iface.mainWindow())
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        layout = self.drop_file_frame.parent().layout()
        self.drop_file_dropzone = DropFrame(self.drop_file_frame.parent())
        self.drop_file_dropzone.setLayout(self.drop_file_frame.layout())

        layout.replaceWidget(self.drop_file_frame, self.drop_file_dropzone)
        self.drop_file_frame.deleteLater()

        self.cancel_button.clicked.connect(self.hide)

    def showEvent(self, event):
        super().showEvent(event)
        self.layer_combobox.setVisible(False)
        self.layer_combobox.clear()
        self.layer_label.setVisible(False)
        self.add_button.setVisible(False)
        
