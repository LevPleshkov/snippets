# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Selector
                                 A QGIS plugin
 Select and display objects
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-10-27
        copyright            : (C) 2022 by lev pleshkvo
        email                : levpleshkov@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Selector class from file Selector.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .selector import Selector
    return Selector(iface)
