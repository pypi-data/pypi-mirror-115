from PySide2 import QtGui

from ciomax.sections.collapsible_section import CollapsibleSection
from ciomax.components.combo_box_grp import ComboBoxGrp
from ciocore import data as coredata
from ciomax import const as k 

class SoftwareSection(CollapsibleSection):
    ORDER = 20

    def __init__(self, dialog):
        """
        Combo box. Renderer

        """
        super(SoftwareSection, self).__init__(dialog, "Software")

        self.component = ComboBoxGrp(label="Software")

        self.content_layout.addWidget(self.component)
        self.configure_combo_box()

        self.component.combobox.currentTextChanged.connect(
            self.on_change)

    def on_change(self, value):
        value =  self.component.combobox.currentText() 
        self.dialog.store.set_renderer_version(value)
        advanced_section = self.dialog.main_tab.section("AdvancedSection")
        advanced_section.on_renderer_change()
        general_section = self.dialog.main_tab.section("GeneralSection")
        general_section.set_instance_type_model()


    def populate_from_store(self):
        store = self.dialog.store
        super(SoftwareSection, self).populate_from_store(store)

        partial_path =  store.renderer_version()
        partial_path = self.dialog.render_scope.closest_version(partial_path)
        self.component.set_by_text(partial_path)
        

    def configure_combo_box(self):

        full_paths = self.dialog.render_scope.package_paths

        model = QtGui.QStandardItemModel()
        for path in full_paths:
            partial_path = path.split("/")[-1]
            model.appendRow(QtGui.QStandardItem(partial_path))
        self.component.set_model(model)

    def resolve(self, _, **kwargs):
        """
        Return software IDs.
        """
        if not coredata.valid():
            return   {}
        tree_data = coredata.data()["software"]
        full_path = self.get_full_software_path()
        package = tree_data.find_by_path(full_path)
        package_ids =  [package["package_id"]]

        return {"software_package_ids": package_ids}

    def get_full_software_path(self):
        partial_path = self.component.combobox.currentText() 
        package_paths = self.dialog.render_scope.package_paths
        return next((p for p in package_paths if p.endswith(partial_path)), None)
