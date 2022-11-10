from qgis.PyQt.QtWidgets import QDialogButtonBox


class BoundaryEditor:
    dialog = None

    @classmethod
    def open(cls, dialog, layer, feature):
        cls.dialog = dialog
        cls.edit_layer = layer
        cls.edit_feature = feature

    @classmethod
    def create_content(cls):
        button_box = cls.dialog.findChild(QDialogButtonBox, 'buttonBox')
        button_box.accepted.connect(cls.accepted)

    @classmethod
    def accepted(cls):
        print('Accept edit')


def open_form(dialog, layer, feature):
    BoundaryEditor.open(dialog, layer, feature)
