import json
from typing import Dict, List, Any
import os 

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItem
from qgis.PyQt.QtCore import Qt, QMetaType,  QDate, QDateTime, QTime
from PyQt5.QtCore import QObject
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsFeature,
    QgsJsonUtils,
    QgsField,
    QgsFields,
    NULL
)

from usemaps_lite.tools.base_logic_class import BaseLogicClass
from usemaps_lite.ui.import_layer import ImportLayerDialog
from usemaps_lite.tools.event_handler import Event
from usemaps_lite.tools.gpkg_handler import GpkgHandler
from usemaps_lite.tools.user_mapper import USER_MAPPER
from usemaps_lite.tools.translations import TRANSLATOR

class Layers(BaseLogicClass, QObject):
    """
    Klasa obsługująca logikę związaną z warstwami
    1. wgrywanie plików GPKG do organizacji
    2. wczytywanie warstw organizacji do QGIS
    3. edycja warstw
    4. usuwanie warstw
    """

    def __init__(self, dockwidget: QtWidgets.QDockWidget):

        QObject.__init__(self, dockwidget)
        BaseLogicClass.__init__(self, dockwidget)

        self.dockwidget.layers_listview.selectionModel().selectionChanged.connect(self.on_layers_listview_selection_changed)
        self.dockwidget.layers_listview.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.dockwidget.layers_listview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dockwidget.layers_listview.doubleClicked.connect(self.get_selected_layer)

        self.dockwidget.remove_layer_button.clicked.connect(self.remove_selected_layer)
        self.dockwidget.remove_layer_button.setEnabled(False)

        self.import_layer_dialog = ImportLayerDialog()

        self.import_layer_dialog.drop_file_dropzone.file_dropped.connect(self.handle_gpkg_file_response)
        self.import_layer_dialog.select_file_button.clicked.connect(self.browse_gpkg_file)
        self.import_layer_dialog.add_button.clicked.connect(self.handle_selected_gpkg_layer_from_dialog)

        self.dockwidget.import_layer_button.clicked.connect(self.import_layer_dialog.show)

        self.event_handler.register_event_handler(Event.DELETED_LAYER, self.handle_deleted_layer_event)
        self.event_handler.register_event_handler(Event.UPLOADED_LAYER, self.handle_uploaded_layer_event)
        self.event_handler.register_event_handler(Event.EDITED_LAYER, self.handle_edited_layer_event)
        self.event_handler.register_event_handler(Event.CHANGED_LIMIT, self.handle_changed_limit_event)

        self.gpkg_handler = GpkgHandler()

    def get_selected_layer(self, index) -> None:
        """
        Wykonuje request pobrania geojsona wybranej warstwy.
        """

        selected_layer = index.sibling(index.row(), 0)
        selected_layer_uuid = selected_layer.data(Qt.UserRole)

        self.selected_layer_name = selected_layer.data()
        self.selected_layer_type = selected_layer.data(Qt.UserRole + 1)
        self.selected_layer_uuid = selected_layer_uuid

        self.api.get(
            f"org/layers/{selected_layer_uuid}/geojson",
            callback=self.handle_load_geojson_response
        )

    def handle_load_geojson_response(self, response: Dict[str, Any]) -> None:
        """
        Wczytuje pobrany geojson wybranej warstwy do projektu w QGIS.
        """

        if (error_msg := response.get("error")) is not None:
            self.show_error_message(f"{TRANSLATOR.translate_error('load layer')}: {error_msg}")
            return

        data = response.get("data")

        layer = QgsVectorLayer(f"{self.selected_layer_type.capitalize()}?crs=EPSG:4326", self.selected_layer_name, "memory")
        provider = layer.dataProvider()

        fields = QgsFields()

        example_props = data["features"][0].get("properties", {})
        for key, value in example_props.items():
            value_type = type(value)
            if value_type == int:
                fields.append(QgsField(key, QMetaType.Int))
            elif value_type == float:
                fields.append(QgsField(key, QMetaType.Double))
            else:
                fields.append(QgsField(key, QMetaType.QString))

        provider.addAttributes(fields)
        layer.updateFields()

        for feat_data in data["features"]:
            feat = QgsFeature()
            feat.setFields(fields)

            attributes = []
            for field in fields:
                attributes.append(feat_data["properties"].get(field.name()))
            feat.setAttributes(attributes)

            geometry = QgsJsonUtils.geometryFromGeoJson(json.dumps(feat_data.get("geometry")))
            feat.setGeometry(geometry)

            provider.addFeatures([feat])

        layer.updateExtents()
        layer.beforeCommitChanges.connect(self.update_layer)

        project = QgsProject.instance()
        custom_variables = project.customVariables()
        stored_mappings = custom_variables.get("usemaps_lite/id") or ''
        mappings = json.loads(stored_mappings) if stored_mappings else {}    

        layer_qgis_id = layer.id()
        
        if layer_qgis_id not in mappings:
            mappings[layer_qgis_id] = self.selected_layer_uuid
            custom_variables["usemaps_lite/id"] = json.dumps(mappings)
            project.setCustomVariables(custom_variables)

        project.addMapLayer(layer)

    def browse_gpkg_file(self) -> None:
        """
        Wyświetla dialog do wskazania pliku GPKG do importu.
        """

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.dockwidget,
            TRANSLATOR.translate_ui("select_file"),
            "",
            TRANSLATOR.translate_ui("file_filter")
        )
        if file_path:
            self.handle_gpkg_file_response(file_path)


    def handle_gpkg_file_response(self, file_path) -> None:
        """
        Weryfikuje wybrany plik GPKG.
        """

        self.current_gpkg_file_path = file_path

        layer_infos = self.gpkg_handler.get_layer_info(self.current_gpkg_file_path)

        if len(layer_infos) == 1:
            # TYLKO JEDNA WARSTWA: przekaż oryginalny plik GPKG
            self.upload_layer_to_api(file_path, is_temp_file=False)
            return
        else:
            # WIELE WARSTW: wyświetl combobox z wyborem warstw
            for info in layer_infos:
                self.import_layer_dialog.layer_combobox.addItem(info.get('icon'), info.get('name'))

            self.import_layer_dialog.layer_combobox.setVisible(True)
            self.import_layer_dialog.layer_label.setVisible(True)
            self.import_layer_dialog.add_button.setVisible(True)

    def handle_selected_gpkg_layer_from_dialog(self) -> None:
        """
        Obsługuje wgranie wybranej warstwy z GPKG.
        """

        selected_layer_name = self.import_layer_dialog.layer_combobox.currentText()

        uri = f"{self.current_gpkg_file_path}|layername={selected_layer_name}"

        temp_gpkg_path = self.gpkg_handler.extract_layer_to_temp_gpkg(uri, selected_layer_name)

        self.upload_layer_to_api(temp_gpkg_path, is_temp_file=True)

    def upload_layer_to_api(self, file_path_to_upload: str, is_temp_file: bool) -> None:
        """
        Ogólna metoda do wysyłania pliku
        (oryginalnego GPKG lub tymczasowo wyodrębnionej warstwy)
        do Usemaps Lite.
        """

        self.api.post_file(
            endpoint="org/upload",
            file_path=file_path_to_upload,
            callback=self.handle_upload_response_and_cleanup(file_path_to_upload, is_temp_file)
        )

    def handle_upload_response_and_cleanup(self, file_path_to_clean: str, is_temp_file: bool):
        """
        Obsługuje odpowiedź po próbie wgrania pliku gpkg.
        """
        def callback_func(response: Dict[str, Any]):
            if (error_msg := response.get("error")) is not None:
                self.show_error_message(f"{TRANSLATOR.translate_error('import layer')}: {error_msg}")
            else:
                self.import_layer_dialog.hide()

            # Sprzątanie: usuń plik TYLKO jeśli był to plik tymczasowy
            if is_temp_file and os.path.exists(file_path_to_clean):
                os.remove(file_path_to_clean)

        return callback_func

    def remove_selected_layer(self):
        """
        Wykonuje request usunięcia z organizacji wybranej warstwy.
        """
        
        reply = QMessageBox.question(
            self.dockwidget,
            TRANSLATOR.translate_ui("remove layer label"),
            TRANSLATOR.translate_ui("remove user question"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            selected_index = self.dockwidget.layers_listview.selectedIndexes()
            uuid = selected_index[0].data(Qt.UserRole)

            self.api.delete(
                "org/layers",
                {"uuid": uuid},
                callback=self.handle_delete_layer_response
            )

    def handle_delete_layer_response(self, response: Dict[str, Any]) -> None:
        """
        Obsługuje odpowiedź po próbie usunięcia warstwy.
        """

        if (error_msg := response.get("error")) is not None:
            self.show_error_message(f"{TRANSLATOR.translate_error('remove layer')}: {error_msg}")


    def on_layers_listview_selection_changed(self) -> None:
        """
        Prosta kontrolka włączająca guzik usuwania warstw
        w momencie zaznaczenie warstwy na liście.
        """

        selected_indexes = self.dockwidget.layers_listview.selectedIndexes()
        has_selection = bool(selected_indexes)
        self.dockwidget.remove_layer_button.setEnabled(has_selection)

    def update_layer(self) -> None:
        """
        Wykonuje request aktualizacji edytowanej warstwy.
        """

        layer = self.sender()
        edit_buffer = layer.editBuffer()

        project = QgsProject.instance()
        custom_variables = project.customVariables()
        stored_mappings = custom_variables.get("usemaps_lite/id") or ''
        mappings = json.loads(stored_mappings) if stored_mappings else {}    

        layer_uuid = mappings.get(layer.id())

        payload = {"uuid": layer_uuid}

        to_add = self.get_added_features(edit_buffer)
        if to_add:
            payload['inserted'] = to_add

        to_update = self.get_updated_features(layer, edit_buffer)
        if to_update:
            payload['updated'] = to_update

        to_delete = self.get_deleted_features(edit_buffer)
        if to_delete:
            payload['deleted'] = to_delete

        self.api.post(
            "org/layers",
            payload,
            callback=self.handle_update_layer_response
        )

    def handle_update_layer_response(self, response: Dict[str, Any]) -> None:
        """
        Obsługuje odpowiedź po próbie zapisu zmian w warstwie.
        """

        if (error_msg := response.get("error")) is not None:
            self.show_error_message(f"{TRANSLATOR.translate_error('edit layer')}: {error_msg}")
            return        

    def get_added_features(self, edit_buffer) -> Dict[str, Any]:
        """ 
        Zwraca słownik z dodanymi obiektami do warstwy
        """

        added_features = edit_buffer.addedFeatures().values()

        features_data = []

        for feature in added_features:
            if feature.hasGeometry():
                f = feature.__geo_interface__
                features_data.append(f)
            else:
                attributes = feature.attributes()
                names = feature.fields().names()
                properties = {names[i]: self.sanetize_data_type(attributes[i]) if attributes[i] != NULL else None
                              for i in range(len(names))}

                features_data.append(properties)

        return features_data

    def get_deleted_features(self, edit_buffer) -> List[int]:
        """
        Zwraca listę z ID usuniętych obiektów z warstwy
        """

        qgis_deleted_features_ids = edit_buffer.deletedFeatureIds()
        return qgis_deleted_features_ids

    def get_updated_features(self, layer, edit_buffer) -> Dict[str, Any]:
        """
        Zwraca słownik z edytowanymi obiektami w warstwie.
        """

        changed_attributes = edit_buffer.changedAttributeValues()
        changed_geometries = edit_buffer.changedGeometries()

        fids = list(set(list(changed_attributes.keys()) +
                    list(changed_geometries.keys())))

        features = []

        for feature in layer.getFeatures(fids):
            if feature.hasGeometry():
                f = feature.__geo_interface__
                f['id'] = feature.id()
                features.append(f)

            else:
                attributes = feature.attributes()
                names = feature.fields().names()
                properties = {names[i]: self.sanetize_data_type(attributes[i]) if attributes[i] != NULL else None
                              for i in range(len(names))}

                features.append({
                    'properties': properties,
                    'id': feature.id()
                })

        return features
    
    def sanetize_data_type(self, value: Any) -> str:
        """
        Formatuje wybrane typy danych do string.
        """

        if isinstance(value, QDateTime):
            value = value.toString('yyyy-MM-dd hh:mm:ss')
        elif isinstance(value, QDate):
            value = value.toString('yyyy-MM-dd')
        elif isinstance(value, QTime):
            value = value.toString('hh:mm:ss')
        return value

    def connect_layersremoved_signal(self, connect: bool):
        """
        Podłącza/rozłącza sygnał aktualizujący zmienną z mapowaniem id załadowanych warstw.
        """
        if connect:
            QgsProject.instance().layersRemoved.connect(self.remove_layer_from_projects_mappings)
        else:
            QgsProject.instance().layersRemoved.disconnect(self.remove_layer_from_projects_mappings)

    def remove_layer_from_projects_mappings(self, layer_qgis_ids: List[str]):
        project = QgsProject.instance()
        custom_variables = project.customVariables()
        stored_mappings = custom_variables.get("usemaps_lite/id") or ''
        mappings = json.loads(stored_mappings) if stored_mappings else {}    

        for layer_qgis_id in layer_qgis_ids:
            if layer_qgis_id in mappings:
                del mappings[layer_qgis_id]

        custom_variables["usemaps_lite/id"] = json.dumps(mappings)
        project.setCustomVariables(custom_variables)

    def handle_deleted_layer_event(self, event_data: Dict[str, Any]) -> None:
        """
        Obsługuje przychodzące zdarzenie usunięcia warstwy z organizacji.
        """

        data = event_data.get("data")
        layer_uuid = data.get("uuid")
        layer_name = data.get("name")
        
        row_to_remove = -1
        
        for layer_row in range(self.dockwidget.layers_model.rowCount()):
            item = self.dockwidget.layers_model.item(layer_row, 0)
            if item and item.data(Qt.UserRole) == layer_uuid:
                row_to_remove = layer_row
                break
        
        if row_to_remove != -1:
            self.dockwidget.layers_model.removeRow(row_to_remove)

        user_email = USER_MAPPER.get_user_email(event_data.get("user"))

        self.show_info_message(f"{user_email} {TRANSLATOR.translate_info('removed layer')} {layer_name}")

    def handle_uploaded_layer_event(self, event_data: Dict[str, Any]) -> None:
        """
        Obsługuje przychodzące zdarzenie wgrania warstwy do organizacji.
        """

        data = event_data.get("data")
        
        layer_name = data.get("name")
        layer_uuid = data.get("uuid")
        layer_type = data.get("type")

        layer_item = QStandardItem(layer_name)
        layer_item.setData(layer_uuid, Qt.UserRole)
        layer_item.setData(layer_type, Qt.UserRole + 1)

        row = [
            layer_item
        ]

        self.dockwidget.layers_model.appendRow(row)

        user_email = USER_MAPPER.get_user_email(event_data.get("user"))

        self.show_info_message(f"{user_email} {TRANSLATOR.translate_ui('added layer')} {layer_name}")

    def handle_edited_layer_event(self, event_data: Dict[str, Any]) -> None:
        """
        Obsługuje przychodzące zdarzenie edycji warstwy z organizacji.
        """

        data = event_data.get("data")
        layer_name = data.get("name")
        layer_uuid = data.get("uuid")

        user_email = USER_MAPPER.get_user_email(event_data.get("user"))

        self.refresh_layer(layer_uuid)
        
        self.show_info_message(f"{user_email} {TRANSLATOR.translate_info('edited layer')} {layer_name}")

    def refresh_layer(self, layer_uuid: str) -> None:
        """
        Pobiera najnowszą wersję warstwy
        """

        project = QgsProject.instance()
        custom_variables = project.customVariables()
        stored_mappings = custom_variables.get("usemaps_lite/id") or ''
        mappings = json.loads(stored_mappings) if stored_mappings else {}    

        layer_qgis_id = next((layer_qgis_id for layer_qgis_id, mapped_layer_uuid in mappings.items() if mapped_layer_uuid == layer_uuid), None)

        if not layer_qgis_id:
            # zaktualizowana warstwa nie jest wczytana do qgis, skip
            return

        self.refreshed_layer = project.mapLayer(layer_qgis_id)
        
        if self.refreshed_layer.isEditable():
            # zaktualizowana warstwa jest aktualnie przez nas edytowana, nie nadpisujemy jej
            return

        self.api.get(
            f"org/layers/{layer_uuid}/geojson",
            callback=self.handle_refresh_layer_response
        )

    def handle_refresh_layer_response(self, response: Dict[str, Any]) -> None:

        provider = self.refreshed_layer.dataProvider()

        # odpinamy sygnał zeby nie robic zbednych strzalow do zapisu zmian
        self.refreshed_layer.beforeCommitChanges.disconnect(self.update_layer)

        self.refreshed_layer.startEditing()

        all_ids = [f.id() for f in self.refreshed_layer.getFeatures()]
        provider.deleteFeatures(all_ids)

        fields = self.refreshed_layer.fields()
        new_features = []

        data = response.get("data")

        for feat_data in data["features"]:
            feat = QgsFeature()
            feat.setFields(fields)

            attributes = [feat_data["properties"].get(field.name()) for field in fields]
            feat.setAttributes(attributes)

            geometry = QgsJsonUtils.geometryFromGeoJson(json.dumps(feat_data.get("geometry")))
            feat.setGeometry(geometry)

            new_features.append(feat)

        provider.addFeatures(new_features)
        self.refreshed_layer.commitChanges()
        self.refreshed_layer.updateExtents()

        # przypinamy znowu
        self.refreshed_layer.beforeCommitChanges.connect(self.update_layer)

    def handle_changed_limit_event(self, event_data: Dict[str, Any]) -> None:
        """
        Obsługuje przychodzące zdarzenie zmiany wykorzystanego limitu danych w organizacji.
        """
        
        data = event_data.get("data")
        value = data.get("limitUsed")
        
        self.dockwidget.limit_progressbar.setValue(value)
