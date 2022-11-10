# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Selector
                                 A QGIS plugin
 Select and display objects
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-10-27
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Lev Pleshkov
        email                : levpleshkov@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsProject, QgsLayerTreeLayer, QgsEditFormConfig
# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .selector_dockwidget import SelectorDockWidget
import os.path
from typing import List

import selector.layer_utils as lu
import selector.map_tools as mt


class Selector:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.project = QgsProject.instance()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Selector_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Selector')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Selector')
        self.toolbar.setObjectName(u'Selector')

        print("** INITIALIZING Selector")
        self.selected_layer = None
        self.rectangle_maptool = mt.RectangleMapTool(self.iface.mapCanvas())

        self.work_dir = os.path.dirname(os.path.realpath(__file__))

        self.pluginIsActive = False
        self.dockwidget = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Selector', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/selector/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

    # --------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        print("** CLOSING Selector")

        self.rectangle_maptool.clean()

        if self.selected_layer:
            self.selected_layer.setSubsetString('')

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crash
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        print("** UNLOAD Selector")

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Selector'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    # --------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            print("** STARTING Selector")

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget is None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = SelectorDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.TopDockWidgetArea, self.dockwidget)

            self.project = QgsProject.instance()
            self.layers = self.project.mapLayers()
            self.layer_names = [layer.name() for layer in self.layers.values()]
            self.selected_layer = None

            self.dockwidget.comboBox.addItems([''] + self.layer_names)
            self.dockwidget.comboBox.currentIndexChanged.connect(self.handle_layer_change)
            self.dockwidget.pushButton.clicked.connect(self.do_query)

            self.dockwidget.btnLoadProject.clicked.connect(self.load_project)
            self.dockwidget.btnCheckPlacement.clicked.connect(self.check_lot)
            self.dockwidget.btnPlaceLot.clicked.connect(self.draw_rectangle)

            self.dockwidget.show()

    def load_project(self):
        work_dir = '/Users/levpleshkov/Documents/Курс QGIS & Python/snippets/qgis плагин'
        gpkg_path = os.path.join(work_dir, 'database', 'perm_krai.gpkg')
        style_path = os.path.join(work_dir, 'styles')
        crs = self.iface.mapCanvas().mapSettings().destinationCrs()

        layers_info: List[lu.LayerInfo] = [
            lu.LayerInfo(gpkg_path, 'boundary', 'Граница ПК', 'boundary.qml', True),
            lu.LayerInfo(gpkg_path, 'districts', 'Границы МО', 'districts.qml', True)
        ]

        for i, layer in enumerate(layers_info):
            layer_to_add = lu.create_layer_from_gpkg(gpkg_path, layer.source_layer, layer.node_name, crs)
            lu.set_layer_style(layer_to_add, layer.style, style_path)
            self.project.addMapLayer(layer_to_add, False)
            tree_node = QgsLayerTreeLayer(layer_to_add)
            lu.set_layer_node_visibility(tree_node, True)
            self.project.layerTreeRoot().insertChildNode(i, tree_node)

            if layer.source_layer == 'boundary':
                form_config = layer_to_add.editFormConfig()
                form_path = os.path.join(self.work_dir, 'forms', 'editForm.ui')
                form_config.setUiForm(form_path)
                form_config.setInitCodeSource(QgsEditFormConfig.CodeSourceFile)
                form_config.setInitFilePath(os.path.join(self.work_dir, 'layer_utils', 'edit_form_check.py'))
                form_config.setInitFunction('open_form')

                layer_to_add.setEditFormConfig(form_config)

        print('Project loaded')

    def check_lot(self):
        pass

    def draw_rectangle(self):
        self.iface.mapCanvas().setMapTool(self.rectangle_maptool)

    def handle_layer_change(self, index):
        if self.selected_layer:
            layer_name = self.layer_names[index]
            self.selected_layer = self.project.mapLayersByName(layer_name)[0]
            # print(self.selected_layer)

    def do_query(self):
        features = self.selected_layer.selectedFeatures()
        if len(features) == 0:
            return

        fids = [feature.id() for feature in features]
        exp = ', '.join([str(fid) for fid in fids])
        query = f'fid in ({exp})'

        self.selected_layer.setSubsetString(query)
